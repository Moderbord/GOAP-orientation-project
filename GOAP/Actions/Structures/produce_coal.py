import game_time as time

from GOAP.action import GOAPAction

class ProduceCoal(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.finished = False

        # local variables
        self.target_resource = "Coal"
        self.message_on_finish = "finished producing coal."
        self.progress = 0
        self.duration = 4

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("isWorked", True)
        self.add_precondition("hasMaterials", True)
        
        # effects
        self.add_effect("hasProduce", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False
        self.progress = 0

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
        self.progress += time.clock.delta

        # TODO wait until materials arrive / is available
        # if self.progress >= self.duration:
        #     print(type(agent).__name__ + " " + self.message_on_finish)
        #     self.finished = True
        #     agent.produce.append("Coal")

        return True