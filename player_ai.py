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

    def Update(self):
        self.fsm.Update()

        if self.current_task is None and not self.task_list.empty():
            self.current_task = self.task_list.get()

        self.Check_Current_Task() # TODO move elsewhere

    def Check_Current_Task(self):
        if not self.current_task:
            return

        entity_group = self.current_task[0]
        entity_type = self.current_task[1]
        target_amount = self.current_task[2]
        entity_class = entities.To_Class(entity_type)

        if entity_group == "Resource":
            if self.Has_Resource(entity_class, target_amount):
                self.current_task = None
        elif entity_group == "Structure":
            if self.Has_Structure(entity_class):
                self.current_task = None
        elif entity_group == "Unit":
            if self.Has_Unit(entity_class, target_amount):
                self.current_task = None
            elif self.Can_Create_Entity(entity_group, entity_type):
                self.Add_Unit(entity_class)


    def Update_Task_List(self):
        if not self.current_goal:
            return
        self.task_list = algorithms.Queue()
        (product_group, product_class, product_amount) = self.current_goal
        self.Queue_Requirements(g_vars[product_group][product_class], product_amount)
        self.task_list.put([product_group, product_class, product_amount])

    def Queue_Requirements(self, target, amount=1):
        if not target["Production"]:
            return

        production_list = target["Production"]
        for product in production_list:
            entity_group = product[0]           # Unit, Structure
            entity_type = product[1]            # Worker, Explorer, Smithy, etc.
            target_amount = product[2]          # How many is needed/ordered
            self.Queue_Requirements(g_vars[entity_group][entity_type], target_amount)
            self.task_list.put([entity_group, entity_type, target_amount])

    def Can_Create_Entity(self, entity_group, entity_type):
        requirement_list = g_vars[entity_group][entity_type]["Production"]
        for requirement in requirement_list:
            required_class = entities.To_Class(requirement[1])  # type of entity
            required_amount = requirement[2]                    # resource needed
            if requirement[0] == "Resource":
                if not self.Has_Resource(required_class, required_amount):
                    return False
            elif requirement[0] == "Structure":
                if not self.Has_Structure(required_class):
                    return False
            elif requirement[0] == "Unit":
                if not self.Has_Unit(required_class, required_amount):
                    return False
        return True

    def Has_Structure(self, target):
        for structure in self.structure_list:
            if isinstance(structure, target):
                return True
        return False

    def Has_Resource(self, target, count=1):
        for resource in self.resource_list:
            if isinstance(resource, target):
                if resource[1] >= count:
                    return True
        return False

    def Has_Unit(self, target, count=1):
        for unit in self.unit_list:
            if isinstance(unit, target):
                count -= 1
            if count is 0:
                return True
        return False

    def Add_Resource(self, resource):
        for owned_resource in self.resource_list:
            if owned_resource[0] is resource[0]: # already has resource
                owned_resource[1] += resource[1] # increment owned resource
                return
        self.resource_list.append(resource)      # else add it to list

    def Add_Unit(self, unit):
        self.unit_list.append(unit(self))

    def Add_Resource_Tile(self, tile):
        self.resource_tiles.append(tile)