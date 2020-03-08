import state_machine as fsm
import message_dispatcher as dispatch
import game_entities as entities
import algorithms
import ai_state
import entity_state
from game_settings import g_vars


class AI:
    def __init__(self, gamemap, start_position):
        self.gamemap = gamemap
        self.start_position = start_position
        self.fsm = fsm.StateMachine(self)
        self.fsm.globalState = ai_state.AIGlobalState()
        self.fsm.currentState = ai_state.AIStateIdle()
        self.dispatcher = dispatch.MessageDispatcher()
        self.unit_list = []
        self.structure_list = []
        self.resource_list = []
        self.resource_tiles = []
        self.current_goal = ()
        self.current_task = None
        self.task_list = algorithms.Queue()

    def update(self):
        self.fsm.update()

        if self.current_task is None and not self.task_list.empty():
            self.current_task = self.task_list.get()

        self.check_current_task() # TODO move elsewhere

    def check_current_task(self):
        if not self.current_task:
            return

        entity_group = self.current_task[0]
        entity_type = self.current_task[1]
        target_amount = self.current_task[2]
        entity_class = entities.to_class(entity_type)

        if entity_group == "Resource":
            if self.has_resource(entity_class, target_amount):
                self.current_task = None
        elif entity_group == "Structure":
            if self.has_structure(entity_class):
                self.current_task = None
        elif entity_group == "Unit":
            if self.has_unit(entity_class, target_amount):
                self.current_task = None
            elif self.can_create_entity(entity_group, entity_type):
                new_unit = entity_class(self)
                new_unit.begin_production()
                self.add_unit(new_unit)

    def update_task_list(self):
        if not self.current_goal:
            return
        self.task_list = algorithms.Queue()
        (product_group, product_class, product_amount) = self.current_goal
        self.queue_requirements(g_vars[product_group][product_class], product_amount)
        self.task_list.put([product_group, product_class, product_amount])

    def queue_requirements(self, target, amount=1):
        if not target["Production"]:
            return

        production_list = target["Production"]
        for product in production_list:
            entity_group = product[0]           # Unit, Structure
            entity_type = product[1]            # Worker, Explorer, Smithy, etc.
            target_amount = product[2]          # How many is needed/ordered
            self.queue_requirements(g_vars[entity_group][entity_type], target_amount)
            self.task_list.put([entity_group, entity_type, target_amount])

    def can_create_entity(self, entity_group, entity_type):
        requirement_list = g_vars[entity_group][entity_type]["Production"]
        for requirement in requirement_list:
            required_class = entities.to_class(requirement[1])  # type of entity
            required_amount = requirement[2]                    # resource needed
            if requirement[0] == "Resource":
                if not self.has_resource(required_class, required_amount):
                    return False
            elif requirement[0] == "Structure":
                if not self.has_structure(required_class):
                    return False
            elif requirement[0] == "Unit":
                if not self.has_unit(required_class, required_amount):
                    return False
        return True

    def has_structure(self, target):
        for structure in self.structure_list:
            if isinstance(structure, target):
                return True
        return False

    def has_resource(self, target, count=1):
        for resource in self.resource_list:
            if isinstance(resource, target):
                if resource[1] >= count:
                    return True
        return False

    def has_unit(self, target, count=1):
        for unit in self.unit_list:
            if isinstance(unit, target):
                count -= 1
            if count <= 0:
                return True
        return False

    def add_resource(self, resource):
        for owned_resource in self.resource_list:
            if owned_resource[0] is resource[0]: # already has resource
                owned_resource[1] += resource[1] # increment owned resource
                return
        self.resource_list.append(resource)      # else add it to list

    def add_unit(self, unit):
        self.unit_list.append(unit)

    def add_resource_tile(self, tile):
        self.resource_tiles.append(tile)

    def get_unit(self, target):
        for unit in self.unit_list:
            if isinstance(unit, target):
                return unit

    def remove_unit(self, target):
        for unit in self.unit_list:
            if unit is target:
                self.unit_list.remove(unit)
                unit.delete()
                return