from random import randint

import ai_state
import algorithms
import entity_state
import game_entities as entities
import message_dispatcher as dispatch
import state_machine as fsm
from game_settings import g_vars


class AI:
    def __init__(self, gamemap, start_position):
        self.gamemap = gamemap
        self.start_position = start_position
        self.fsm = fsm.StateMachine(self)
        self.fsm.globalState = ai_state.AIGlobalState()
        self.fsm.currentState = ai_state.AIStateIdle()
        self.dispatcher = dispatch.MessageDispatcher()
        self.entity_list = []
        self.production_list = []
        self.resource_map = {}
        self.current_goal = []
        self.current_task = None
        self.target_resource = None
        self.task_list = algorithms.Queue()
        self.time_since_lask_task_update = 0

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
            
        if target_group == "Exploration":
            # has not found resource
            if not self.has_found_resource(target_class, target_amount):
                # explore
                if not self.fsm.is_in_state(ai_state.AIStateExplore):
                    self.fsm.change_state(ai_state.AIStateExplore())
            # has found resource
            else:
                # has found enough materials
                if self.has_resource(g_vars[target_group][target_type]["GatheredType"][1], target_amount):
                    # done
                    self.complete_current_task()
                # has not found enough materials
                else:
                    # gather
                    if not self.fsm.is_in_state(ai_state.AIStateGather):
                        self.fsm.change_state(ai_state.AIStateGather())
                    self.target_resource = (target_group, target_type, target_class)
            return

        else:
            if self.has_num_entities(target_class, target_amount):
                self.complete_current_task()
            elif self.can_create_entity(target_group, target_type):
                new_entity = target_class(self)
                new_entity.begin_production()
                self.deduct_resource_cost(g_vars[target_group][target_type]["Production"])
            else:
                self.prepend_goal(self.current_task)
            return

    def complete_current_task(self):
        if self.current_task == self.current_goal[0]:
            self.current_goal.remove(self.current_task)
        self.current_task = None
        # tasks has been updated
        self.time_since_lask_task_update = 0

    def update_task_list(self): # Not used atm
        if not self.current_goal:
            return
        self.task_list = algorithms.Queue()
        # loop through current goal(s)
        for goal in self.current_goal:
            (target_group, target_class, target_amount) = goal
            # get all requirements
            task_list = self.get_requirements(g_vars[target_group][target_class], target_amount)
            # re-queue them
            while not task_list.empty():
                self.task_list.put(task_list.get())
            # given task need to be put as last task
            self.task_list.put([target_group, target_class, target_amount])
        # clear current task
        self.current_task = None
        # tasks has been updated
        self.time_since_lask_task_update = 0

    def append_goal(self, goal):
        # check so last goal isn't identical
        if len(self.current_goal) > 0 and self.current_goal[-1] == goal:
            return
        self.current_goal.append(goal)
        # get tasks
        task_list = self.get_tasks_from_goal(goal)
        # append tasks to current queue
        while not task_list.empty():
            self.task_list.put(task_list.get())
        # tasks has been updated
        self.time_since_lask_task_update = 0

    def prepend_goal(self, goal):
        # check so first goal isn't identical
        if len(self.current_goal) > 0 and self.current_goal[0] == goal:
            return
        self.current_goal.insert(0, goal)
        # get tasks
        task_list = self.get_tasks_from_goal(goal)
        # append current queue to new queue
        while not self.task_list.empty():
            task_list.put(self.task_list.get())
        # re-assign
        self.task_list = task_list
        # current task then needs to be cleared
        self.current_task = None
        # tasks has been updated
        self.time_since_lask_task_update = 0

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
            # already completed -> skip
            if self.has_num_entities(entities.to_class(target_type), target_amount):
                continue
            # chain multiplikation
            if not target_group == "Structure":
                target_amount *= amount         
            # get sub-requirements
            self.get_requirements(g_vars[target_group][target_type], target_amount, task_list)
            task_list.put([target_group, target_type, target_amount])

        return task_list

#--------------------------Entities--------------------------#

    def can_create_entity(self, target_group, target_type):
        production_list = g_vars[target_group][target_type]["Production"]
        for target in production_list:
            target_class = entities.to_class(target[1])  # type of entity
            target_amount = target[2]                    # resource needed
            if target[0] == "Resource":
                if not self.has_resource(target[1], target_amount):
                    return False
            elif target[0] == "Structure":
                if not self.has_available_structure(target_class):
                    # structure should not be occupied
                    return False
            elif target[0] == "Unit":
                if not self.has_available_unit(target_class, target_amount):
                    # unit should not be locked or similiar
                    return False
            elif target[0] == "Exploration":
                return False

        return True

    def entities_where(self, function):
        return [e for e in self.entity_list if function(e)]

    def entities_count_where(self, function, count=1):
        entity_list = [e for e in self.entity_list if function(e)]
        return entity_list[:count]

    def add_entity(self, entity):
        self.entity_list.append(entity)
        print("\nAdded entity: " + str(entity))

    def remove_entity(self, target):
        self.entity_list.remove(target)
        target.delete()
        print("Removed entity: " + str(target))      

    def has_num_entities(self, target, count=1):
        # check own entities
        for entity in self.entity_list:
            if isinstance(entity, target):
                count -= 1
        # check what is currently udner production
        for entity in self.production_list:
            if isinstance(entity, target):
                count -= 1
        if count <= 0:
            return True
        return False

#--------------------------UNITS--------------------------#

    def has_unit(self, target, count=1):
        for unit in self.entity_list:
            if isinstance(unit, target) and unit.is_visible:
                count -= 1
            if count <= 0:
                return True
        return False
        
    def has_available_unit(self, target, count=1):
        for unit in self.entity_list:
            if isinstance(unit, target) and unit.is_idle:
                count -= 1
            if count <= 0:
                return True
        return False

    def get_available_unit(self, target):
        for unit in self.entity_list:
            if isinstance(unit, target) and unit.is_idle:
                return unit

    def get_available_units(self, target, count=1):
        unit_list = []
        for unit in self.entity_list:
            if isinstance(unit, target) and unit.is_idle:
                unit_list.append(unit)
                count -= 1
            if count <= 0:
                return unit_list
        return unit_list 

#--------------------------STRUCTURES--------------------------#

    def has_available_structure(self, target):
        for structure in self.entity_list:
            if isinstance(structure, target) and structure.is_idle:
                return True
        return False

    def get_available_structure(self, target):
        for structure in self.entity_list:
            if isinstance(structure, target) and structure.is_idle:
                return structure   

    def get_buildable_tile(self):
        radius = 4
        # search for buildable locations around starting position
        buildable_tiles = self.gamemap.get_buildable_area(self.start_position, radius)
        # increase search radius 
        while not buildable_tiles:
            radius += 1
            buildable_tiles = self.gamemap.get_buildable_area(self.start_position, radius)
        # choose one of the available tiles
        index = randint(0, len(buildable_tiles) - 1)
        return buildable_tiles[index]

#--------------------------RESOURCES--------------------------#

    def add_resource(self, resource):
        for x in range(0, resource[0][2]): # amount
            new_resource = entities.to_class(resource[0][1])
            self.add_entity(new_resource(self))

    def has_resource(self, target, count=1):
        target_class = entities.to_class(target)
        for resource in self.entity_list:
            if isinstance(resource, target_class):
                count -= 1
            if count <= 0:
                return True
        return False

    def has_found_resource(self, target, count=1):
        for resource_tile in self.resource_map.values():
            for resource in resource_tile.resource_list:
                if isinstance(resource, target):
                    count -= 1
                if count <= 0:
                    return True
        return False

    def get_resource_location(self, worker_location, target):
        # find matching resources
        matches = []
        for location, resource_tile in self.resource_map.items():
            for resource in resource_tile.available_resources:
                if isinstance(resource, target):
                    matches.append(location)
        # no matches
        if not matches:
            return None
        # sort matches by Manhattan from worker location
        sorted_matches = sorted(matches, key=lambda cord: (abs(cord[0] - worker_location[0]) + abs(cord[1] - worker_location[1])))
        return sorted_matches[0]

    def deduct_resource_cost(self, resource_list):
        for resource_cost in resource_list:
            target_group = resource_cost[0]
            target_class = entities.to_class(resource_cost[1])
            target_amount = resource_cost[2]
            # only resources should be deducted
            if not target_group == "Resource":
                continue
            # find correct resource and deduct
            for resource in self.entities_count_where(lambda res: isinstance(res, target_class), target_amount):
                self.remove_entity(resource)