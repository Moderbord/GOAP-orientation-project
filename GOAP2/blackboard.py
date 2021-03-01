
class Blackboard():

    def __init__(self) -> None:
        self.navigation_target = None
        self.navigation_status = False
        self.position = None
        self.movement_speed = 0
        self.movement_factor = 0
        self.new_position = False
        self.replan_requested = False

    def set_navigation_target(self, target):
        self.navigation_target = target

    def get_navigation_target(self):
        return self.navigation_target

    def set_navigation_status(self, status):
        self.navigation_status = status

    def get_navigation_status(self):
        return self.navigation_status

    def set_position(self, value):
        self.position = value
        self.new_position = True

    def get_position(self):
        return self.position

    def set_movement_speed(self, value):
        self.movement_speed = value

    def get_movement_speed(self):
        return self.movement_speed

    def set_movement_factor(self, value):
        self.movement_factor = value

    def get_movement_factor(self):
        return self.movement_factor

    def new_position_notified(self):
        self.new_position = False

    def has_new_position(self):
        return self.new_position

    def request_replan(self):
        self.replan_requested = True

    def is_replan_requested(self):
        return self.replan_requested
    
    
