from mesa import Agent
import numpy as np


class EvacuationAgent(Agent):
    """Schelling segregation agent."""

    def __init__(self, model, starting_move, exit_list, pos):
        """Create a new Schelling agent.

        Args:
            model: The model instance the agent belongs to
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(model)
        self.move = starting_move
        self.exit_list = exit_list
        self.score = 0
        self.moved = False
        self.exit_list = exit_list
        if starting_move:
            self.move = starting_move
        else:
            self.move = self.random.choice(["C", "D"]) # create logic here for how to determine sanity of agent
        self.next_move = None

        # find nearest exit
        distance = 999999999
        self.closest_exit = tuple()
        for exit_pos in exit_list:
            new_distance = np.linalg.norm(np.array(pos) - np.array(exit_pos))
            if (new_distance < distance):
                distance = new_distance
                self.closest_exit = exit_pos


    def step(self) -> None:
        """Determine if agent is happy and move if necessary."""
        if self.pos == None or self.moved:
            return
        if (self.pos == self.closest_exit):
            self.model.grid.remove_agent(self)
            return

        neighbors = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=self.model.radius
        )
        best_pos = self.pos

        #! you might want to put a loop here just in case another agent steals this agent move
        # find empty space that moves toward your closest exit
        for i in neighbors:
            if self.model.grid.is_cell_empty(i):
                if (np.linalg.norm(np.array(best_pos) - np.array(self.closest_exit)) > (np.linalg.norm(np.array(i) - np.array(self.closest_exit)))):
                    best_pos = i


        #! see if any agents want the exit and haven't already moved this round
        #! Chance of moving based on neighbors maybe decide what random number it will be for each overall step in model

        if best_pos != self.pos: # check if have new pos
            self.model.grid.move_agent(self, best_pos)
            self.moved = True
        self.find_nearest_exit() # reevaluate nearest exit


    def reset_moved(self) -> None:
        self.moved = False

    def find_nearest_exit(self) -> None:
        distance = np.linalg.norm(np.array(self.pos) - np.array(self.closest_exit))
        for exit_pos in self.exit_list:
            new_distance = np.linalg.norm(np.array(self.pos) - np.array(exit_pos))
            if (new_distance < distance):
                distance = new_distance
                self.closest_exit = exit_pos