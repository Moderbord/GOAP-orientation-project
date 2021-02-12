from GOAP.Actions.Player.unit_production_action import UnitProductionAction
from GOAP.Agents.worker import Worker

class ProduceWorker(UnitProductionAction):

    def __init__(self):
        super().__init__()
        self.production_target = Worker

        self.duration = 5

        self.add_precondition("freeWorkerSlot", True)

        self.add_effect("hasWorker", True)
        self.add_effect("hasFreeWorker", True)
        