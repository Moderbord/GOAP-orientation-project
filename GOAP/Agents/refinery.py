from random import randint
from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.action_set import ActionSet
from GOAP.game_actor import GameActor
from GOAP.Agents.artisan import Profession

# Actions
from GOAP.Actions.Structures.produce_coal import ProduceCoal
from GOAP.Actions.Structures.create_build_job import CreateBuildJob
from GOAP.Actions.Structures.create_work_job import CreateWorkJob
from GOAP.Actions.Structures.create_fetch_job import CreateFetchJob

class Refinery(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Structure"]["Base"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        GameActor.__init__(self)
        self.position.x = randint(1, 6)
        self.position.y = randint(1, 6)
        
        # local variables
        self.raw_materials = []
        self.produce = []
        self.is_built = False
        self.is_worked = False
        self.has_materials = False
        self.required_materials = {"Logs" : 2}
        self.required_artisan = Profession.Refiner
        self.build_time = 3

        # actions
        self.add_action(ProduceCoal())
        self.add_action(CreateBuildJob())
        self.add_action(CreateWorkJob())
        self.add_action(CreateFetchJob())

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = {}
        #
        world_data["isBuilt"] = self.is_built
        world_data["isWorked"] = self.is_worked
        world_data["hasMaterials"] = self.has_materials
        world_data["hasProduce"] = len(self.produce) > 0
        #
        return world_data

    def create_goal_state(self):        
        goal_state = ActionSet()
        goal_state.add("produceCoal", True)

        return goal_state

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)

    def on_resource_change(self):
        self.has_materials = all([self.raw_materials.count(key) >= self.required_materials.get(key) for key in self.required_materials.keys()]) # <3

    def on_built(self):
        self.is_built = True
        self.tile_color = g_vars["Structure"]["Refinery"]["TileColor"]
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        print("Refinery built!")

    def on_worked(self):
        self.is_worked = True
        print("Refinery operational!")

    def on_fetched(self, resource):
        self.raw_materials.append(resource)
        self.on_resource_change()        

    def on_collected(self):
        if len(self.produce) > 0:
            self.produce.pop()
            return True
        else:
            print("ERROR NO PRODUCE COLLECTED")
            return False
