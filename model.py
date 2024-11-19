from mesa import Model
from mesa.datacollection import DataCollector
from agents import SchellingAgent
from mesa.space import SingleGrid
import numpy as np
import matplotlib.pyplot as plt

# Function to display the grid
def plot_grid(grid, title="Agent Distribution"):
    grid_array = np.zeros((grid.height, grid.width))
    for cell in grid.coord_iter():
        cell_content, loc = cell
        x, y = loc
        if cell_content is not None:
            grid_array[y][x] = cell_content.type  # Use agent's type for coloring
    plt.figure(figsize=(8, 8))
    plt.imshow(grid_array, cmap="viridis", origin="upper")
    plt.title(title)
    plt.colorbar(label="Agent Type")
    plt.show()



class Schelling(Model):
    """Model class for the Schelling segregation model."""

    def __init__(
        self,
        height: int = 40,
        width: int = 40,
        density: float = 0.8,
        minority_pc: float = 0.5,
        homophily: int = 3,
        radius: int = 1,
        seed=None,
    ):
        """Create a new Schelling model.

        Args:
            width: Width of the grid
            height: Height of the grid
            density: Initial chance for a cell to be populated (0-1)
            minority_pc: Chance for an agent to be in minority class (0-1)
            homophily: Minimum number of similar neighbors needed for happiness
            radius: Search radius for checking neighbor similarity
            seed: Seed for reproducibility
        """
        super().__init__(seed=seed)

        # Model parameters
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.radius = radius

        # Initialize grid
        self.grid = SingleGrid(width, height, torus=True)

        # Track happiness
        self.happy = 0

        # Set up data collection
        self.datacollector = DataCollector(
            model_reporters={
                "happy": "happy",
                "pct_happy": lambda m: (m.happy / len(m.agents)) * 100
                if len(m.agents) > 0
                else 0,
                "population": lambda m: len(m.agents),
                "minority_pct": lambda m: (
                    sum(1 for agent in m.agents if agent.type == 1)
                    / len(m.agents)
                    * 100
                    if len(m.agents) > 0
                    else 0
                ),
            },
            agent_reporters={"agent_type": "type"},
        )

        # Create agents and place them on the grid
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < minority_pc else 0
                agent = SchellingAgent(self, agent_type)
                self.grid.place_agent(agent, pos)

        # Collect initial state
        self.datacollector.collect(self)

    def step(self):
        """Run one step of the model."""
        self.happy = 0  # Reset counter of happy agents
        self.agents.shuffle_do("step")  # Activate all agents in random order
        self.datacollector.collect(self)  # Collect data
        self.running = self.happy < len(self.agents)  # Continue until everyone is happy


model = Schelling()
steps = 10
plot_grid(model.grid, title="Initial Agent Distribution")
for step in range(steps):
    model.step()

plot_grid(model.grid, title="Final Agent Distribution")
