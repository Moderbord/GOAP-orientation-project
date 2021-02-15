from random import randint

import game_time as time

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.transform import Position
from GOAP.action_set import ActionSet

# Actions
from GOAP.Actions.Player.produce_worker import ProduceWorker
from GOAP.Actions.Player.assign_worker_logs import AssignWorkerLogs
from GOAP.Actions.Player.assign_worker_ore import AssignWorkerOre
from GOAP.Actions.Player.gather_resources import GatherResources

class EntityTable():

    def __init__(self):
        self.__table = {}

    # def add_entity(self, entity):
    #     value = self.__table.get(entity, None)

    #     if value:
    #         value.append(entity)
    #     else


class Player(GOAPAgent, GOAPProvidable):

    def __init__(self, game_map, starting_location=Position()):
        super().__init__()
        self.data_provider = self
        self.resources = []
        self.units = []
        self.structures = []
        self.game_map = game_map
        self.starting_location = starting_location

        # actions
        # self.add_action(ProduceWorker())
        # self.add_action(AssignWorkerLogs())
        # self.add_action(AssignWorkerOre())
        # self.add_action(GatherResources())

    def update(self):
        for unit in self.units:
            unit.update()
        for structure in self.structures:
            structure.update()
        super().update()

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = ActionSet()
        #
        # workers = self.count_units("Worker")
        # world_data.add("canCreateWorker", workers < 3)
        #
        # free_workers = self.count_unit_type_where("Worker", lambda x: x.goal_state is None)
        # world_data.add("hasFreeWorker", free_workers > 0)
        #
        return world_data

    def create_goal_state(self):
        goal_state = ActionSet()
        goal_state.add("gatherResources", True)
        goal_state.add("haveFreeWorker", True)

        return goal_state

    # def resolve_goal(self, action_effects):
    #     for key, value in action_effects.items():
    #         if not self.goal_state.get(key) == value:
    #             continue
    #         else:
    #             self.goal_state.pop(key)

    def add_unit(self, unit):
        unit.owner = self
        unit.start_agent() # GOAP
        unit.groups = self.game_map.sprite_group_units
        unit.start_actor() # Draw
        self.units.append(unit)
    
    def add_structure(self, structure):
        structure.owner = self
        structure.start_agent() # GOAP
        structure.groups = self.game_map.sprite_group_structures
        structure.start_actor() # Draw
        self.structures.append(structure)

    def get_units(self, unit):
        return [x for x in self.units if type(x).__name__ == unit]

    def get_units_where(self, function):
        return [x for x in self.units if function(x)]

    def get_unit_type_where(self, unit, function):
        return [x for x in self.get_units(unit) if function(x)]

    def count_units(self, unit):
        return len([x for x in self.units if type(x).__name__ == unit])

    def count_unit_type_where(self, unit, function):
        return len([x for x in self.get_units(unit) if function(x)])

    def get_structure(self, target):
        structure = [x for x in self.structures if type(x).__name__ == target]
        return structure[0] if structure else None

    def get_structure_where(self, function):
        structure = [x for x in self.structures if function(x)]
        return structure[0] if structure else None

    def add_resource(self, resource):
        self.resources.append(resource)

    def remove_resource(self, resource, amount=1):
        if self.resources.count(resource) >= amount:
            for i in amount:
                self.resources.remove(resource)
            return True
        
        print("Not enough resources to deduct!")
        return False

    def count_resource(self, resource):
        return len([x for x in self.resources if type(x).__name__ == resource])

    def get_resource_drop_off_loc(self):
        return Position(1, 1)
    
    def get_resource_location(self, resource):
        if resource == "Ore":
            return Position(randint(8, 10), randint(2, 4))
        elif resource == "Logs":
            return Position(randint(1, 4), randint(6, 9))

    def plan_found(self, goal, actions):
        pass

    def actions_finished(self):
        pass


