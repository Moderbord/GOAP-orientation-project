from game_settings import g_vars

from GOAP.transform import Position
from GOAP.Agents.structure import Structure
from GOAP.action_set import ActionSet

# Actions
from GOAP.Actions.Structures.pickup_production_job import PickupProductionJob
from GOAP.Actions.Structures.produce_soldier import ProduceSoldier
from GOAP.Actions.Structures.create_build_job import CreateBuildJob
from GOAP.Actions.Structures.create_fetch_job import CreateFetchJob

class Encampment(Structure):

    def __init__(self):
        Structure.__init__(self)
        self.position = Position(8, 1)

        # local variables
        self.structure_name = "Encampment"
        self.construction_time = 3
        self.construction_materials = {"Logs" : 10}

        # production
        self.production_table = {"Soldier" : {"Sword" : 1}}

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