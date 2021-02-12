import game_time as time

from GOAP.action import GOAPAction
from GOAP.transform import Position

class GatherAction(GOAPAction):

    def __init__(self):
        super().__init__()
        self.finished = False
        self.target_resource = None
        self.message_on_finish = None

        self.progress = 0
        self.duration = 0

    def reset(self):
        super().reset()
        self.finished = False
        self.progress = 0

    def requires_in_range(self):
        return True

    def completed(self):
        return self.finished

    def check_precondition(self, agent):
        # Search for nearest tree
        self.target = agent.owner.get_resource_location(self.target_resource)
        return True

    def perform(self, agent):
        self.progress += time.clock.delta

        if self.progress >= self.duration:
            print(type(agent).__name__ + " " + self.message_on_finish)
            self.finished = True
            agent.backpack.append(self.target_resource)

        return True