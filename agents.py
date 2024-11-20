from mesa import Agent


class SchellingAgent(Agent):
    """Schelling segregation agent."""

    def __init__(self, model, agent_type: int) -> None:
        """Create a new Schelling agent.

        Args:
            model: The model instance the agent belongs to
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(model)
        self.type = agent_type

    def step(self) -> None:
        """Determine if agent is happy and move if necessary."""
        neighbors = self.model.grid.iter_neighbors(
            self.pos, moore=True, radius=self.model.radius
        )

        new_pos = (self.pos[0] - 1, self.pos[1])
        if self.pos[0] != 0 and self.model.grid.is_cell_empty(new_pos):
            self.model.grid.move_agent(self, new_pos)
        # else:
        #     self.model.grid.remove_agent(self)

        # # Count similar neighbors
        # similar = sum(neighbor.type == self.type for neighbor in neighbors)
        #
        # # If unhappy, move to a random empty cell:
        # if similar < self.model.homophily:
        #     self.model.grid.move_to_empty(self)
        # else:
        #     self.model.happy += 1

        # if self.model.grid.is_cell_empty(self.pos[0]-1,self.pos[1]):
        #     self.modle.grid.move_agent(self.pos[0]-1,self.pos[1])
