from mesa import Agent
import numpy as np
import random


class EvacuationAgent(Agent):

    def __init__(self, model, starting_move, pos):
        """Create a new agent.

        Args:
            model: The model instance the agent belongs to
            starting_move: Is the agent a deflector or cooperator on start
            pos: agent position on board 
        """
        super().__init__(model)
        self.move = starting_move
        self.score = 0
        self.moved = False
        if starting_move:
            self.move = starting_move
        else:
            self.move = self.random.choice(["C", "D"]) # create logic here for how to determine sanity of agent
        self.next_move = None

        # find nearest exit
        distance = 999999999
        self.closest_exit = tuple()
        for exit_pos in self.model.exit_list:
            new_distance = np.linalg.norm(np.array(pos) - np.array(exit_pos))
            if (new_distance < distance):
                distance = new_distance
                self.closest_exit = exit_pos


    def step(self) -> None:
        """Determine if agent is happy and move if necessary."""
        if self.pos == None or self.moved:
            return

        potential_move = True # default check variable
        while potential_move:

            # find empty space that moves toward your closest exit
            best_pos = self.find_best_move()

            if best_pos == self.pos: # check if have new pos
                return


            # see if any agents want the exit and haven't already moved this round
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=1)
            potential_movers = []
            for i in neighbors:
                if (not i.moved) and (best_pos) == (i.find_best_move()): # find their own current best move
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
                if len(cooperators) > 0: # update status of cooperators that lost the opportunity to win the spot
                    for i in cooperators:
                        if random.randint(0, self.model.conflict_strategy_inertia - 1) == 0:
                            i.move = "D"
                chance = len(defectors) * self.model.deflector_penalty # 2 is penalty but can create variable alter
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


    def reset_moved(self) -> None:
        self.moved = False


    def exit(self) -> None:
        if self.pos == self.closest_exit and self.model.count_agents() > 1:
            self.model.grid.remove_agent(self)
        elif self.pos == self.closest_exit:
            self.model.done = True


    def find_nearest_exit(self) -> None:
        distance = np.linalg.norm(np.array(self.pos) - np.array(self.closest_exit))
        for exit_pos in self.model.exit_list:
            new_distance = np.linalg.norm(np.array(self.pos) - np.array(exit_pos))
            if (new_distance < distance):
                distance = new_distance
                self.closest_exit = exit_pos


    def find_best_move(self):
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, radius=self.model.radius)
        best_pos = self.pos
        best_distance = np.linalg.norm(np.array(self.pos) - np.array(self.closest_exit))

        for neighbor_pos in neighborhood:
            if self.model.grid.is_cell_empty(neighbor_pos):
                # Calculate the distance from the neighbor to the closest exit
                distance_to_exit = np.linalg.norm(np.array(neighbor_pos) - np.array(self.closest_exit))

                # If the neighbor is closer to the exit, set it as the best position
                if distance_to_exit < best_distance:
                    best_pos = neighbor_pos
                    best_distance = distance_to_exit

        return best_pos
