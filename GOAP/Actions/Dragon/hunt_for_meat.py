import random

import game_time as time

from GOAP.action import GOAPAction
from GOAP.transform import Position

class HuntForMeat(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.cost = 35

        # local variables
        self.finished = False
        self.hunting_duration = 5
        self.progress = 0

        # preconditions
        self.add_precondition("isHungry", True)
        
        # effects
        self.add_effect("hasMeat", True)
        self.add_effect("isHome", False)

    def reset(self):
        super().reset()
        # reset local variables
        self.finished = False
        self.progress = 0

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        area = 10
        self.target = Position(random.randint(area, area * 2), random.randint(area, area * 2))
        return True

    def perform(self, agent):
        # perform the action
        self.progress += time.clock.delta

        if self.progress >= self.hunting_duration:
            print(type(agent).__name__ + " finished hunting.")
            self.finished = True
            agent.backpack.append("Meat")

        return True
        