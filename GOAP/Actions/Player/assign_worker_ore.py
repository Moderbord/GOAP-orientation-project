from GOAP.Actions.Player.assign_worker_action import AssignWorkerAction

class AssignWorkerOre(AssignWorkerAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.target_command = "collectOre"

        # effects
        self.add_effect("hasOre", True)
