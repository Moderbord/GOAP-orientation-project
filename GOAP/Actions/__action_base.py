from GOAP.action import GOAPAction

class __Base(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        # self.target = None
        # self.in_range = False
        # self.minimun_range = 0
        # self.cost = 1.0

        # loval variables

        # preconditions
        
        # effects

    def reset(self):
        super().reset()
        # reset local state
        # self.target = None
        # self.in_range = False

    def requires_in_range(self):
        # does action require agent to be in range
        pass

    # def get_cost(self):
    #     # returns the intrinsic cost of the action
    #     return self.cost

    def completed(self):
        # is action completed
        pass

    def check_precondition(self, agent):
        # check for any required criterias for the action
        pass

    def perform(self, agent):
        # perform the action
        pass