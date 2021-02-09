import game_time as time

from GOAP.action import GOAPAction

class WaitForMeat(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.waiting_limit = 5
        self.time_elapsed = 0

        # preconditions
        self.add_precondition("isHome", True)
        self.add_precondition("hasWaited", False)
        
        # effects
        self.add_effect("hasMeat", True)

    def reset(self):
        super().reset()
        # reset local variables
        self.finished = False
        self.time_elapsed = 0

    def requires_in_range(self):
        # does action require agent to be in range
        return False

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        return True

    def perform(self, agent):
        # perform the action
        self.time_elapsed += time.clock.delta

        if self.time_elapsed >= self.waiting_limit:
            print("NO MORE WAIT")
            agent.waited_for_food = True
            return False

        if agent.backpack.count("Meat") > 0:
            print("FINALLY FOOD")
            self.finished = True

        return True
        