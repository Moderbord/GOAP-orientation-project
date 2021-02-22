import game_time as time

from GOAP.action import GOAPAction
from GOAP.Agents.worker import Worker

class ProduceWorker(GOAPAction):

    def __init__(self):
        super().__init__()
        self.finished = False
        self.production_target = Worker
        self.message_on_finish = "was produced"

        self.progress = 0
        self.duration = 5

        self.add_effect("haveFreeWorker", True)

    def reset(self):
        super().reset()
        self.finished = False
        self.progress = 0

    def requires_in_range(self):
        return False

    def completed(self):
        return self.finished

    def check_precondition(self, agent):
        # Check for free and compatible building
        return True

    def perform(self, agent):
        if agent.count_units("Worker") >= 5:
            self.finished = True
            return True

        self.progress += time.clock.delta

        if self.progress >= self.duration:
            #print(self.production_target.__name__ + " " + self.message_on_finish)
            self.finished = True
            agent.add_unit(self.production_target())

        return True