from GOAP.Actions.Player.assign_worker_action import AssignWorkerAction

class AssignWorkerLogs(AssignWorkerAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.target_command = "collectLogs"

        # effects
        self.add_effect("hasLogs", True)
