from GOAP.Actions.Worker.deliver_action import DeliverAction

class DeliverOre(DeliverAction):

    def __init__(self):
        super().__init__()
        self.finished = False
        self.item = "Ore"

        self.add_precondition("hasOre", True)
        self.add_effect("collectOre", True, 1)
