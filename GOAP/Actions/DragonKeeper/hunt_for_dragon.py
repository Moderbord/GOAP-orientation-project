import game_time as time

from GOAP.action import GOAPAction
from GOAP.transform import Position

class HuntForDragon(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.cost = 50.0
        # local variables
        self.hunted = False
        self.progress = 0
        self.hunting_duration = 15

        # preconditions
        self.add_precondition("dragonIsHungry", True)
        self.add_precondition("dragonIsHome", True)
        
        # effects
        self.add_effect("hasMeat", True)

    def reset(self):
        super().reset()
        # reset local variables
        self.hunted = False
        self.progress = 0

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    def completed(self):
        # is action completed
        return self.hunted

    def check_precondition(self, agent):
        # check for any required criterias for the action
        self.target = Position(3, 25)
        return True

    def perform(self, agent):
        # perform the action
        self.progress += time.clock.delta
        #print("Hunting progress:..." + str(self.progress))

        if self.progress >= self.hunting_duration:
            print(type(agent).__name__ + " finished hunting.")
            self.hunted = True
            agent.backpack.append("Meat")

        return True