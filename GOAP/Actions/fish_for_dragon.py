import random

import game_time as time

from GOAP.action import GOAPAction
from GOAP.transform import Position

class FishForDragon(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.cost = 20.0
        # local variables
        self.fished = False
        self.progress = 0
        self.hunting_duration = 25

        # preconditions
        self.add_precondition("dragonIsHungry", True)
        
        # effects
        self.add_effect("hasMeat", True)

    def reset(self):
        super().reset()
        # reset local variables
        self.fished = False
        self.progress = 0

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    def get_cost(self):
        return random.randint(25, 75)

    def completed(self):
        # is action completed
        return self.fished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        self.target = Position(1, -5)
        return True

    def perform(self, agent):
        # perform the action
        self.progress += time.clock.delta
        #print("Hunting progress:..." + str(self.progress))

        if self.progress >= self.hunting_duration:
            print(type(agent).__name__ + " finished fishing.")
            self.fished = True
            agent.backpack.append("Meat")

        return True