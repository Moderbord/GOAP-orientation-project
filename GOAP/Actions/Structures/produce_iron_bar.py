from GOAP.Actions.Structures.produce_resource import ProduceResource

class ProduceIronBar(ProduceResource):

    def __init__(self):
        super().__init__()
        # production specific
        self.target_resource = "IronBar"
        self.message_on_finish = "finished producing iron bar."
        self.production_time = 5

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("isWorked", True)
        self.add_precondition("hasMaterials", True)
        
        # effects
        self.add_effect("produceIronBar", True)
        