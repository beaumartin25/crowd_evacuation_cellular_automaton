from mesa import Model
from mesa.datacollection import DataCollector
from agents import EvacuationAgent
from mesa.space import SingleGrid
import numpy as np
import matplotlib.pyplot as plt

# Function to display the grid for debugging
def plot_grid(grid, title="Agent Distribution"):
    grid_array = np.zeros((grid.height, grid.width))
    for cell in grid.coord_iter():
        cell_content, loc = cell
        x, y = loc
        if cell_content is not None:
            # Map "C" to 1 and "D" to 2
            grid_array[y][x] = 1 if cell_content.move == "C" else 2
    plt.figure(figsize=(8, 8))
    plt.imshow(grid_array, cmap="viridis", origin="upper")
    plt.title(title)
    plt.colorbar(label="Agent Move (1 = Cooperating, 2 = Defecting)")
    plt.show()



class Evacuation(Model):
    """Model class for the Schelling segregation model."""

    def __init__(
        self,
        height: int = 40,
        width: int = 40,
        density: float = 0.5,
        deflecting_pc: float = 0.5,
        radius: int = 1,
        exit_list: list = [(0,19),(0,20),(0,21)],
        seed=None,
    ):
        """Create a new Schelling model.

        Args:
            width: Width of the grid
            height: Height of the grid
            density: Initial chance for a cell to be populated (0-1)
            deflecting_pc: Chance for an agent start as deflecting
            radius: Search radius for checking neighbor similarity
            seed: Seed for reproducibility
        """
        super().__init__(seed=seed)

        # Model parameters
        self.height = height
        self.width = width
        self.density = density
        self.deflecting_pc = deflecting_pc
        self.radius = radius # I assume will need for later to decide how many neighbors for a empty space in front

        # Initialize grid
        self.grid = SingleGrid(width, height, torus=True)


        #! Set up data collection, ideas: percentage of agents that moved, how many have changed to deflect
        self.datacollector = DataCollector(
            {
                "Cooperating_Agents": lambda m: len(
                    [a for a in m.agents if a.move == "C"]
                )
            }
        )

        # Create agents and place them on the grid
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agent_type = "D" if self.random.random() < deflecting_pc else "C"
                agent = EvacuationAgent(self, agent_type, exit_list, pos)
                self.grid.place_agent(agent, pos)

        # Collect initial state
        self.datacollector.collect(self)

    def step(self):
        """Run one step of the model."""
        self.agents.shuffle_do("step")  # Activate all agents in random order
        self.datacollector.collect(self)  # Collect data
        self.agents.do('reset_moved')

# for debugging code
model = Evacuation()
steps = 10
plot_grid(model.grid, title="Initial Agent Distribution")
for step in range(steps):
    model.step()

plot_grid(model.grid, title="Final Agent Distribution")
