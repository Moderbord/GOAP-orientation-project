from game_settings import g_vars

from GOAP.transform import Position
from GOAP.Agents.structure import Structure
from GOAP.action_set import ActionSet

# Actions
from GOAP.Actions.Structures.pickup_production_job import PickupProductionJob
from GOAP.Actions.Structures.produce_artisan import ProduceArtisan
#from GOAP.Actions.Structures.produce_explorer import ProduceExplorer
#from GOAP.Actions.Structures.produce_worker import ProduceWorker

class Camp(Structure):

    def __init__(self):
        Structure.__init__(self)
        self.position = Position(2, 2)

        # local variables
        self.structure_name = "Camp"
        self.is_built = True

        # production
        self.production_table = {"Worker" : {}, "Artisan" : {}, "Explorer" : {}}
        
        # actions
        self.add_action(PickupProductionJob())
        self.add_action(ProduceArtisan())
        #self.add_action(ProduceExplorer())
        #self.add_action(ProduceWorker())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = { "produce" + p : p == self.production_target for p in self.production_table.keys()}
        world_data["isBuilt"] = self.is_built
        world_data["hasMaterials"] = self.has_materials
        #
        return world_data

    def create_goal_state(self):        
        goal_state = ActionSet()
        goal_state.add("doJob", True)
        return goal_state