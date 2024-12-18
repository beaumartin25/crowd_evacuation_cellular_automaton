from mesa import Model
from mesa.datacollection import DataCollector
from agents import EvacuationAgent
from mesa.space import SingleGrid
import numpy as np
import matplotlib.pyplot as plt


class Evacuation(Model):
    """Model class for the model."""

    def __init__(
        self,
        height: int = 40,
        width: int = 40,
        density: float = 0.8,
        deflecting_pc: float = 0.2,
        radius: int = 1,
        exit_list: list = [(0,19),(0,20),(0,21), (19,0),(20,0),(21,0)],
        deflector_penalty = 2,
        conflict_strategy_inertia=2,
        seed=None,
    ):
        """Create a new model.

        Args:
            width: Width of the grid
            height: Height of the grid
            density: Initial chance for a cell to be populated (0-1)
            deflecting_pc: Chance for an agent start as deflecting
            radius: Search radius for checking neighbor similarity
            exit_list: List of x and y coordinates for exits
            deflector_penalty: penalty inforced if a deflecter plays against other deflectors
            conflict_strategy_inertia: possiblity a cooperator changes to a deflector after losing a opportunity to move
            seed: Seed for reproducibility
        """
        super().__init__(seed=seed)

        # Model parameters
        self.height = height
        self.width = width
        self.density = density
        self.deflecting_pc = deflecting_pc
        self.radius = radius
        self.exit_list = exit_list
        self.deflector_penalty = deflector_penalty
        self.conflict_strategy_inertia = conflict_strategy_inertia
        self.done = False

        # Initialize grid
        self.grid = SingleGrid(width, height, torus=True)

        self.total_exited_agents = 0
        self.step_count = 0

        #! Set up data collection, ideas: percentage of agents that moved, how many have changed to deflect
        self.datacollector = DataCollector(
            {
                "Agents_Moved": lambda m: len([a for a in m.agents if a.moved]),
                "Deflecting_Agents": lambda m: len(
                    [a for a in m.agents if a.move == "D"]),
                "Cooperating_Agents": lambda m: len(
                    [a for a in m.agents if a.move == "C"]
                ),
                "Exited_count": lambda m: self.total_exited_agents,
                "Average_Exited": lambda m: m.update_average_exited(),
            }
        )

        # Create agents and place them on the grid
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agent_type = "D" if self.random.random() < deflecting_pc else "C"
                agent = EvacuationAgent(self, agent_type, pos)
                self.grid.place_agent(agent, pos)

        # Collect initial state
        self.starting_count = self.count_agents()
        self.current_count = self.count_agents()
        self.datacollector.collect(self)

    def update_average_exited(self):
        self.current_count = self.count_agents()
        """Calculate and update the average number of agents exiting."""
        # Get the count of agents who have exited this step

        # Update totals
        self.total_exited_agents = self.starting_count - self.current_count
        self.step_count += 1

        # Calculate and return the average
        return self.total_exited_agents / self.step_count if self.step_count > 0 else 0

    def step(self):
        """Run one step of the model."""
        #agent_count = self.count_agents()
        if not self.done:
            self.agents.shuffle_do("step")  # Activate all agents in random order
            self.agents.do("exit")
            self.datacollector.collect(self)  # Collect data
            self.agents.do("reset_moved")  # Reset moved status for all agents

    def count_agents(self):
        return sum(1 for cell in self.grid.coord_iter() if cell[0] is not None)

