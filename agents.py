from mesa import Agent


class EvacuationAgent(Agent):
    """Schelling segregation agent."""

    def __init__(self, model, starting_move=None):
        """Create a new Schelling agent.

        Args:
            model: The model instance the agent belongs to
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(model)
        self.move = starting_move
        self.score = 0
        if starting_move:
            self.move = starting_move
        else:
            self.move = self.random.choice(["C", "D"]) # create logic here for how to determine sanity of agent
        self.next_move = None


    def step(self) -> None:
        """Determine if agent is happy and move if necessary."""
        neighbors = self.model.grid.iter_neighbors(
            self.pos, moore=True, radius=self.model.radius
        )
        #! Chance of moving based on neighbors maybe decide what random number it will be for each overall step in model


        #! want to set better parameters for what the exit would be
        if self.pos != None:
            new_pos = (self.pos[0] - 1, self.pos[1])
            if self.pos[0] != 0 and self.model.grid.is_cell_empty(new_pos):
                self.model.grid.move_agent(self, new_pos)
            else:
                self.model.grid.remove_agent(self)


