from GOAP.action import GOAPAction
from GOAP.transform import Position

class DeliverOre(GOAPAction):

    def __init__(self):
        super().__init__()
        self.delivered = False

        self.add_precondition("hasOre", True)
        self.add_effect("collectOre", True)

    def reset(self):
        super().reset()
        self.delivered = False

    def requires_in_range(self):
        return True

    def completed(self):
        return self.delivered

    def check_precondition(self, agent):
        # Search for drop off
        self.target = Position(1, 1)
        return True

    def perform(self, agent):
        print("Delivering ore!")
        self.delivered = True
        agent.backpack.remove("Ore")
        return True