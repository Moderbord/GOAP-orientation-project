from GOAP.action import GOAPAction
from GOAP.transform import Position

class FeedDragon(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.cost = 5.0
        # local variables
        self.feed_dragon = False

        # preconditions
        self.add_precondition("hasMeat", True)
        self.add_precondition("dragonIsHome", True)
        
        # effects
        self.add_effect("satisfyDragon", True)

    def reset(self):
        super().reset()
        # reset local variables
        self.feed_dragon = False

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    def completed(self):
        # is action completed
        return self.feed_dragon

    def check_precondition(self, agent):
        # check for any required criterias for the action
        self.target = agent.dragon.home
        return True

    def perform(self, agent):
        # perform the action
        print("Fed dragon <3")
        self.feed_dragon = True
        agent.dragon.backpack.append("Meat")
        agent.backpack.remove("Meat")
        return True