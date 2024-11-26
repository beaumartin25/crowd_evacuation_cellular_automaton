from mesa import Agent
import numpy as np
import random


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

        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, radius=self.model.radius
        )

        #! you might want to put a loop here just in case another agent steals this agents move
        potential_move = True # default check variable
        while potential_move:
            best_pos = self.pos

            # find empty space that moves toward your closest exit
            potential_move = False
            for i in neighborhood:
                if self.model.grid.is_cell_empty(i) and (np.linalg.norm(np.array(best_pos) - np.array(self.closest_exit)) > (np.linalg.norm(np.array(i) - np.array(self.closest_exit)))):
                    best_pos = i
                    potential_move = True

            if best_pos == self.pos: # check if have new pos
                return


            # see if any agents want the exit and haven't already moved this round
            neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=True, radius=1
            )
            potential_movers = []
            for i in neighbors:
                if (not i.moved) and (np.linalg.norm(np.array(best_pos) - np.array(i.closest_exit)) < (np.linalg.norm(np.array(i.pos) - np.array(i.closest_exit)))): #! maybe find their own current best step in a method would add more complexity
                    potential_movers.append(i)


            # Chance of moving based on neighbors
            defectors = [i for i in potential_movers if i.move == "D"]
            cooperators = [i for i in potential_movers if i.move == "C"]
            if len(defectors) == 1: # only 1 defector
                winner = defectors[0]
            elif len(cooperators) == len(potential_movers) or len(potential_movers) == 1: # all coop
                chance = len(potential_movers)
                r_int = random.randint(0,  chance - 1)
                winner = potential_movers[r_int]
            else: # contain multiple deflectors
                chance = len(defectors) * 2 # 2 is penalty but can create variable alter
                r_int = random.randint(0, chance - 1)
                if r_int < len(defectors):
                    winner = defectors[r_int]
                else: # no one moves!
                    return


            # moving and updating status for the winning agent
            self.model.grid.move_agent(winner, best_pos)
            winner.moved = True
            winner.find_nearest_exit() # reevaluate nearest exit

            if self.moved:
                return

            #! update status of cooperators that lost the opportunity to win the spot

    def reset_moved(self) -> None:
        self.moved = False

    def find_nearest_exit(self) -> None:
        distance = np.linalg.norm(np.array(self.pos) - np.array(self.closest_exit))
        for exit_pos in self.exit_list:
            new_distance = np.linalg.norm(np.array(self.pos) - np.array(exit_pos))
            if (new_distance < distance):
                distance = new_distance
                self.closest_exit = exit_pos

