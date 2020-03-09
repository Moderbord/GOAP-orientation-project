from random import randint

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
        self.resource_map = {}
        self.current_goal = []
        self.current_task = None
        self.target_resource = None
        self.task_list = algorithms.Queue()

    def update(self):
        self.fsm.update()

        if self.current_task is None and not self.task_list.empty():
            self.current_task = self.task_list.get()

        self.check_current_task() # TODO move elsewhere

    # Method that checks if progress can be made on current task
    def check_current_task(self):
        if not self.current_task:
            return

        target_group = self.current_task[0]
        target_type = self.current_task[1]
        target_amount = self.current_task[2]
        target_class = entities.to_class(target_type)

        # Exploration group
        if target_group == "Exploration":
            if self.has_found_resource(target_class):
                if not self.fsm.is_in_state(ai_state.AIStateGather):
                    self.fsm.change_state(ai_state.AIStateGather())
                    self.target_resource = (target_group, target_type, target_class)
            else:
                if not self.fsm.is_in_state(ai_state.AIStateExplore):
                    self.fsm.change_state(ai_state.AIStateExplore())
            return

        # Resource group
        if target_group == "Resource":
            if self.has_resource(target_class, target_amount):
                self.current_task = None
            elif self.can_create_entity(target_group, target_type):
                pass
            return
        
        # Structure group
        if target_group == "Structure":
            if self.has_structure(target_class):
                self.current_task = None
            elif self.can_create_entity(target_group, target_type):
                new_structure = target_class(self)
                new_structure.begin_production()
                self.add_structure(new_structure)
            return

        # Unit group
        if target_group == "Unit":
            if self.has_unit(target_class, target_amount):
                self.current_task = None
            elif self.can_create_entity(target_group, target_type):
                new_unit = target_class(self)
                new_unit.begin_production()
                self.add_unit(new_unit)
            return

    def update_task_list(self): # Not used atm
        if not self.current_goal:
            return

        # loop through current goal(s)
        for goal in self.current_goal:
            (target_group, target_class, target_amount) = goal
            # queue all requirements
            self.task_list = self.get_requirements(g_vars[target_group][target_class], target_amount)
            # given task need to be put as last task
            self.task_list.put([target_group, target_class, target_amount])
        # clear current task
        self.current_task = None

    def append_goal(self, goal):
        task_list = self.get_tasks_from_goal(goal)
        # append tasks to current queue
        while not task_list.empty():
            self.task_list.put(task_list.get())

    def prepend_goal(self, goal):
        task_list = self.get_tasks_from_goal(goal)
        # current task isn't in queue and need to be appended
        task_list.put(self.current_task)
        # append current queue to new queue
        while not self.task_list.empty():
            task_list.put(self.task_list.get())
        # re-assign
        self.task_list = task_list
        # current task then needs to be cleared
        self.current_task = None

    def get_tasks_from_goal(self, goal):
        (target_group, target_class, target_amount) = goal
        # get all requirements
        task_list = self.get_requirements(g_vars[target_group][target_class], target_amount)
        # given task need to be put as last task
        task_list.put([target_group, target_class, target_amount])
        return task_list
    
    # Method that will queue requirements recursively and put them in the task list
    def get_requirements(self, target, amount=1, task_list=None):
        if not task_list:
            task_list = algorithms.Queue()

        if not target["Production"]:
            return task_list

        production_list = target["Production"]
        for product in production_list:
            target_group = product[0]           # Unit, Structure
            target_type = product[1]            # Worker, Explorer, Smithy, etc.
            target_amount = product[2]          # How many is needed/ordered
            if not target_group == "Structure":
                target_amount *= amount         # chain multiplikation
            self.get_requirements(g_vars[target_group][target_type], target_amount, task_list)
            task_list.put([target_group, target_type, target_amount])

        return task_list

    def can_create_entity(self, target_group, target_type):
        production_list = g_vars[target_group][target_type]["Production"]
        for target in production_list:
            target_class = entities.to_class(target[1])  # type of entity
            target_amount = target[2]                    # resource needed
            if target[0] == "Resource":
                if not self.has_resource(target_class, target_amount):
                    return False
            elif target[0] == "Structure":
                if not self.has_available_structure(target_class):
                    # structure should not be occupied
                    return False
            elif target[0] == "Unit":
                if not self.has_available_unit(target_class, target_amount):
                    # unit should not be locked or similiar
                    return False
        return True

#--------------------------UNITS--------------------------#

    def add_unit(self, unit):
        self.unit_list.append(unit)

    def has_unit(self, target, count=1):
        for unit in self.unit_list:
            if isinstance(unit, target):
                count -= 1
            if count <= 0:
                return True
        return False
        
    def has_available_unit(self, target, count=1):
        for unit in self.unit_list:
            if isinstance(unit, target) and unit.fsm.is_in_state(entity_state.StateIdle):
                count -= 1
            if count <= 0:
                return True
        return False

    def get_available_unit(self, target):
        for unit in self.unit_list:
            if isinstance(unit, target) and unit.fsm.is_in_state(entity_state.StateIdle):
                return unit  

    def remove_unit(self, target):
        for unit in self.unit_list:
            if unit is target:
                self.unit_list.remove(unit)
                unit.delete()
                return      

    def print_unit_at_location(self, location):
               pass

#--------------------------STRUCTURES--------------------------#

    def add_structure(self, structure):
        self.structure_list.append(structure)

    def has_structure(self, target):
        for structure in self.structure_list:
            if isinstance(structure, target):
                return True
        return False

    def has_available_structure(self, target):
        for structure in self.structure_list:
            if isinstance(structure, target) and structure.fsm.is_in_state(entity_state.StateIdle):
                return True
        return False

    def get_available_structure(self, target):
        for structure in self.structure_list:
            if isinstance(structure, target) and structure.fsm.is_in_state(entity_state.StateIdle):
                return structure   

    def remove_structure(self, target):
        for structure in self.structure_list:
            if structure is target:
                self.unit_list.remove(structure)
                structure.delete()
                return         

    def get_buildable_tile(self): # TODO change to list which is filled when creating the ai
        buildable_tiles = self.gamemap.get_buildable_area(self.start_position, 1)
        index = randint(0, len(buildable_tiles) - 1)
        return buildable_tiles[index]

#--------------------------RESOURCES--------------------------#

    def add_resource(self, resource):
        for owned_resource in self.resource_list:
            if owned_resource[0] is resource[0]: # already has resource
                owned_resource[1] += resource[1] # increment owned resource
                return
        self.resource_list.append(resource)      # else add it to list

    def has_resource(self, target, count=1):
        for resource in self.resource_list:
            if isinstance(resource, target):
                if resource[1] >= count:
                    return True
        return False

    def has_found_resource(self, target):
        for resource_list in self.resource_map.values():
            for resource in resource_list:
                if isinstance(resource, target):
                    return True
        return False

    def get_resource_location(self, target):
        for location, resource_list in self.resource_map.items():
            for resource in resource_list:
                if isinstance(resource, target):
                    return location