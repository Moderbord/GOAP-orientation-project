from GOAP.action import GOAPAction
from GOAP.transform import Position

class DeliverAction(GOAPAction):

    def __init__(self):
        super().__init__()
        self.finished = False
        self.item = None

    def reset(self):
        super().reset()
        self.finished = False

    def requires_in_range(self):
        return True

    def completed(self):
        return self.finished

    def check_precondition(self, agent):
        # Search for drop off
        self.target = agent.owner.get_resource_drop_off_loc()
        return True

    def perform(self, agent):
        
        if agent.backpack.count(self.item) > 0:
            print("Delivered " + self.item + "!")
            self.finished = True
            agent.backpack.remove(self.item)
            agent.owner.add_resource(self.item)
            agent.goal_state = None
            return True
        
        return False