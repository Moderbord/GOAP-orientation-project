from GOAP.action import GOAPAction

class ReturnHome(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.cost = 5.0

        # loval variables
        self.finished = False

        # preconditions
        self.add_precondition("isHome", False)

        # effects
        self.add_effect("isHome", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    # def get_cost(self):
    #     # returns the intrinsic cost of the action
    #     return self.cost

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        self.target = agent.home
        return True

    def perform(self, agent):
        # perform the action
        print("ARRIVED HOME")
        self.finished = True
        return True