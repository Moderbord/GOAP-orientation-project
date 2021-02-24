from game_settings import g_vars

from GOAP.transform import Position
from GOAP.Agents.structure import Structure
from GOAP.action_set import ActionSet
from GOAP.Agents.artisan import Profession

# Actions
from GOAP.Actions.Structures.produce_coal import ProduceCoal
from GOAP.Actions.Structures.create_build_job import CreateBuildJob
from GOAP.Actions.Structures.create_work_job import CreateWorkJob
from GOAP.Actions.Structures.create_fetch_job import CreateFetchJob

class Refinery(Structure):

    def __init__(self):
        Structure.__init__(self)
        self.position = Position(4, 5)

        # local variables
        self.structure_name = "Refinery"
        self.construction_time = 3
        self.construction_materials = {"Logs" : 10}

        # production
        self.production_target = "Coal"
        self.production_table = {"Coal" : {"Logs" : 10}}
        self.required_artisan = Profession.Refiner

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