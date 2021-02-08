import game_time as time

from GOAP.action import GOAPAction
from GOAP.transform import Position

class MineOre(GOAPAction):

    def __init__(self):
        super().__init__()
        self.mined = False

        self.progress = 0
        self.mining_duration = 3

        self.add_effect("hasOre", True)

    def reset(self):
        super().reset()
        self.mined = False
        self.progress = 0

    def requires_in_range(self):
        return True

    def completed(self):
        return self.mined

    def check_precondition(self, agent):
        # Search for nearest ore vein
        self.target = Position(3, 3)
        return True

    def perform(self, agent):
        self.progress += time.clock.delta
        print("Mining progress:..." + str(self.progress))

        if self.progress >= self.mining_duration:
            print(type(agent).__name__ + " finished mining.")
            self.mined = True
            agent.backpack.append("Ore")

        return True