import game_time as time

from GOAP.action import GOAPAction

# Template class for gathering actions
class GatherAction(GOAPAction):

    def __init__(self):
        super().__init__()
        self.finished = False
        self.gathered = False
        self.target_resource = None
        self.message_on_finish = None

        self.progress = 0
        self.duration = 0

        self.add_effect("doWork", True)

    def reset(self):
        super().reset()
        self.finished = False
        self.gathered = False
        self.progress = 0

    def requires_in_range(self):
        return True

    def get_cost(self, agent):
        return 10 + agent.owner.resources.count(self.target_resource)

    def completed(self):
        return self.finished

    def check_precondition(self, agent):
        # Search for nearest resource
        self.target = agent.owner.get_resource_location(self.target_resource)
        return True

    def perform(self, agent):
        # drop off resource
        if self.gathered:
            print("Delivered " + self.target_resource + "!")
            self.finished = True
            agent.backpack.remove(self.target_resource)
            agent.owner.add_resource(self.target_resource)
            return True

        # has gathered -> go to drop off location
        if agent.backpack.count(self.target_resource) > 0:
            self.gathered = True
            self.target = agent.owner.get_resource_drop_off_loc()
            self.in_range = False
            return True

        # gathering
        self.progress += time.clock.delta

        if self.progress >= self.duration:
            print(type(agent).__name__ + " " + self.message_on_finish)
            agent.backpack.append(self.target_resource)

        return True