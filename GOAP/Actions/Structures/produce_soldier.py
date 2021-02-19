from GOAP.Actions.Structures.produce_unit import ProduceUnit

class ProduceSoldier(ProduceUnit):

    def __init__(self):
        super().__init__()
        # production specific
        self.target_unit = "Soldier"
        self.precursor_unit = "Worker"
        self.message_on_finish = "finished producing soldier."
        self.production_time = 5

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("hasMaterials", True)
        self.add_precondition("produceSoldier", True)
        
        # effects
        self.add_effect("doJob", True)
