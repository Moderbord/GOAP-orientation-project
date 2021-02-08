from GOAP.action import GOAPAction

class BurnSubject(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.cost = 10
        
        # local variables
        self.finished = False

        # preconditions
        self.add_precondition("isBored", True)
        
        # effects
        self.add_effect("staySatisfied", True)

    def reset(self):
        super().reset()
        # reset local variables
        self.finished = False

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
        print("BURNING SUBJECT... *CRISP*")
        self.finished = True
        agent.boredom = 0
        return True