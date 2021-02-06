import game_time as time
import GOAP.action as action
import GOAP.transform as transform

class MineOre(action.GOAPAction):

    def __init__(self):
        super().__init__()
        self.mined = False

        self.__progress = 0
        self.mining_duration = 3

        self.add_effect("hasOre", True)
        self.add_effect("collectOre", True)

    def reset(self):
        super().reset()
        self.mined = False
        self.__progress = 0

    def requires_in_range(self):
        return True

    def completed(self):
        return self.mined

    def check_precondition(self, agent):
        # Search for nearest ore vein
        self.target = transform.Position(3, 3)
        return True

    def perform(self, agent):
        self.__progress += time.clock.delta
        print("Mining progress:..." + str(self.__progress))

        if self.__progress >= self.mining_duration:
            print(type(agent).__name__ + " finished mining.")
            self.mined = True
            agent.backpack.append("Ore")

        return True