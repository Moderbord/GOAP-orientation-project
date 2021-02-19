from GOAP.transform import Position
from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet
from GOAP.game_actor import GameActor

from GOAP.Agents.soldier import Soldier

# Actions
from GOAP.Actions.Structures.pickup_production_job import PickupProductionJob
from GOAP.Actions.Structures.produce_soldier import ProduceSoldier
from GOAP.Actions.Structures.create_build_job import CreateBuildJob
from GOAP.Actions.Structures.create_fetch_job import CreateFetchJob

class Encampment(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Structure"]["Base"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        GameActor.__init__(self)
        self.position = Position(8, 1)
        
        # local variables
        self.structure_name = "Encampment"
        self.construction_materials = {"Logs" : 10}
        self.build_time = 3
        self.is_built = False

        # production
        self.raw_materials = []
        self.production_table = {"Soldier" : {"Sword" : 1} }

        # action specific
        self.production_target = ""
        self.production_target_requirements = {}
        self.has_materials = False
        self.production_ready = False

        # actions
        self.add_action(PickupProductionJob())
        self.add_action(ProduceSoldier())
        self.add_action(CreateBuildJob())
        self.add_action(CreateFetchJob())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = { "produce" + p : p == self.production_target for p in self.production_table.keys()}
        world_data["isBuilt"] = self.is_built
        world_data["hasMaterials"] = self.has_materials
        #
        return world_data

    def create_goal_state(self):        
        goal_state = ActionSet()
        goal_state.add("isBuilt", True)
        goal_state.add("doJob", True)

        return goal_state

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)

    def on_resource_change(self):
        # production/building material requirement
        self.production_target_requirements = self.production_table.get(self.production_target, {}) if self.is_built else self.construction_materials
        # count materials for given target
        self.has_materials = all([self.raw_materials.count(key) >= self.production_target_requirements.get(key) for key in self.production_target_requirements.keys()])

    def on_built(self):
        self.is_built = True
        self.raw_materials.clear()
        self.has_materials = False

        self.tile_color = g_vars["Structure"][self.structure_name]["TileColor"]
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        print(self.structure_name + " built!")

    def on_fetched(self, resource):
        self.raw_materials.append(resource)
        self.on_resource_change()      
    
    def on_production_begin(self):
        self.production_ready = True

        for material, amount in self.production_target_requirements.items():
            for x in range(amount):
                self.raw_materials.remove(material)

    def on_production_finish(self, produced_unit):
        if self.production_target != produced_unit:
            print("PRODUCTION ERROR!! WRONG UNIT NOT PRODUCED")
            return

        # reset
        self.on_resource_change()
        self.production_target = "" 
        self.production_ready = False

        new_unit = None
        if produced_unit == "Soldier":
            new_unit = Soldier()

        new_unit.position = Position(self.position.x, self.position.y)
        self.owner.add_unit(new_unit)