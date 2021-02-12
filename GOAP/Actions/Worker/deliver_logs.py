from GOAP.Actions.Worker.deliver_action import DeliverAction

class DeliverLogs(DeliverAction):

    def __init__(self):
        super().__init__()
        self.finished = False
        self.item = "Logs"

        self.add_precondition("hasLogs", True)
        self.add_effect("collectLogs", True, 1)

