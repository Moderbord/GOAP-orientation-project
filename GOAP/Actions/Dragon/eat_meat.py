from GOAP.action import GOAPAction

class EatMeat(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.has_eaten = False

        # preconditions
        self.add_precondition("hasMeat", True)
        
        # effects
        self.add_effect("stayAlive", True)

    def reset(self):
        super().reset()
        # reset local variables
        self.has_eaten = False

    def requires_in_range(self):
        # does action require agent to be in range
        return False

    def completed(self):
        # is action completed
        return self.has_eaten

    def check_precondition(self, agent):
        # check for any required criterias for the action
        return True

    def perform(self, agent):
        # perform the action
        print("EATING.... *CHOMP*")
        self.has_eaten = True
        agent.hunger = 0
        agent.backpack.remove("Meat")
        return True