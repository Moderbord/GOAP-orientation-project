from GOAP.Actions.Worker.gather_action import GatherAction

class GatherLogs(GatherAction):

    def __init__(self):
        super().__init__()
        self.target_resource = "Logs"
        self.message_on_finish = "chopped wood."

        self.duration = 5