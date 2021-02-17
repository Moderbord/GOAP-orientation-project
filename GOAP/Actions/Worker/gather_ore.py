from GOAP.Actions.Worker.gather_action import GatherAction

class GatherOre(GatherAction):

    def __init__(self):
        super().__init__()
        self.target_resource = "Ore"
        self.message_on_finish = "mined ore."

        self.duration = 3
        