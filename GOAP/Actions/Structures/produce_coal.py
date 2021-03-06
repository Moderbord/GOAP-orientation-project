from GOAP.Actions.Structures.produce_resource import ProduceResource

class ProduceCoal(ProduceResource):

    def __init__(self):
        super().__init__()
        # production specific
        self.target_resource = "Coal"
        self.message_on_finish = "finished producing coal."
        self.production_time = 4

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("isWorked", True)
        self.add_precondition("hasMaterials", True)
        
        # effects
        self.add_effect("produceCoal", True)