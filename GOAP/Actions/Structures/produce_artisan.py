from GOAP.Actions.Structures.produce_unit import ProduceUnit

class ProduceArtisan(ProduceUnit):

    def __init__(self):
        super().__init__()
        # production specific
        self.target_unit = "Artisan"
        self.precursor_unit = "Worker"
        self.message_on_finish = "finished producing artisan."
        self.production_time = 5

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("produceArtisan", True)
        
        # effects
        self.add_effect("doJob", True)
        