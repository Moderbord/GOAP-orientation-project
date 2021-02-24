from GOAP.transform import Position
from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet
from GOAP.game_actor import GameActor

# Actions
from GOAP.Actions.Structures.pickup_production_job import PickupProductionJob
from GOAP.Actions.Structures.produce_artisan import ProduceArtisan
#from GOAP.Actions.Structures.produce_explorer import ProduceExplorer
#from GOAP.Actions.Structures.produce_worker import ProduceWorker

class Camp(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Structure"]["Camp"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        GameActor.__init__(self)
        self.position = Position(2, 2)
        
        # local variables
        self.structure_name = "Camp"
        self.is_built = True

        # production
        self.raw_materials = []
        self.production_table = {"Worker" : {}, "Artisan" : {}, "Explorer" : {}}

        # action specific
        self.production_target = ""
        self.production_target_requirements = {}
        self.has_materials = False
        self.production_ready = False

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

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)

    def on_resource_change(self):
        self.production_target_requirements = self.production_table.get(self.production_target, {})
        self.has_materials = all([self.raw_materials.count(key) >= self.production_target_requirements.get(key) for key in self.production_target_requirements.keys()])

    def on_fetched(self, resource):
        self.raw_materials.append(resource)
        self.on_resource_change() 

    def on_production_begin(self):
        self.production_ready = True
    
        for material, amount in self.production_target_requirements.items():
            for x in range(amount):
                self.raw_materials.remove(material)