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
        self.add_precondition("isHome", True)
        
        # effects
        self.add_effect("staySatisfied", True)

    def reset(self):
        super().reset()
        # reset local variables
        self.finished = False

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        self.target = agent.home
        
        if agent.subjects > 0:
            return True

        return False

    def perform(self, agent):
        # perform the action
        print("BURNING SUBJECT... *CRISP*")
        self.finished = True
        agent.boredom = 0
        agent.subjects -= 1
        return True