
class Blackboard():

    def __init__(self) -> None:
        self.inventory = []
        self.navigation_target = None
        self.navigation_status = False
        self.manual_navigation = False
        self.target_fact_type = None
        self.target_object = None
        self.position = None
        self.movement_speed = 0
        self.movement_factor = 0
        self.new_position = False
        self.replan_requested = False
        self.timed_action_progress = 0.0
        self.doing_timed_action = False

    # inventory
    def add_object(self, object):
        self.inventory.append(object)

    def remove_object(self, object):
        self.inventory.remove(object) # TODO check first

    def has_object(self, object):
        return object in self.inventory

    # navigation
    def set_navigation_target(self, target):
        self.navigation_target = target

    def get_navigation_target(self):
        return self.navigation_target

    def set_navigation_status(self, status):
        self.navigation_status = status

    def get_navigation_status(self):
        return self.navigation_status

    def has_navigation_status(self, value):
        return self.navigation_status == value

    def set_manual_navigation_target(self, target):
        self.manual_navigation = True
        self.navigation_target = target

    def set_manual_navigation(self, value):
        self.manual_navigation = value

    def has_manual_navigation(self):
        return self.manual_navigation

    # position
    def set_position(self, value):
        self.position = value
        self.new_position = True

    def get_position(self):
        return self.position

    def new_position_notified(self):
        self.new_position = False

    def has_new_position(self):
        return self.new_position

    # movement
    def set_movement_speed(self, value):
        self.movement_speed = value

    def get_movement_speed(self):
        return self.movement_speed

    def set_movement_factor(self, value):
        self.movement_factor = value

    def get_movement_factor(self):
        return self.movement_factor
    
    # memory
    def set_target_fact_type(self, target):
        self.target_fact_type = target

    def get_target_fact_type(self):
        return self.target_fact_type

    def set_target_object_type(self, target):
        self.target_object = target

    def get_target_object_type(self):
        return self.target_object

    # planning
    def set_request_replan(self, value):
        self.replan_requested = value

    def is_replan_requested(self):
        return self.replan_requested

    # timed action
    def add_progress_time(self, time):
        self.timed_action_progress += time

    def get_progress_time(self):
        return self.timed_action_progress

    def began_timed_action(self):
        return self.doing_timed_action

    def begin_timed_action(self):
        self.doing_timed_action = True

    def reset_timed_progress(self):
        self.doing_timed_action = False
        self.timed_action_progress = 0.0


#####
    
class BlackboardManager():

    def __init__(self) -> None:
        self.agent_table = {}

    def create_blackboard(self, agent_id: int) -> Blackboard:
        blackboard = Blackboard()
        self.agent_table[agent_id] = blackboard
        return blackboard

    def get_blackboard(self, agent_id: int) -> Blackboard:
        return self.agent_table.get(agent_id)

g_bbm = BlackboardManager()