
class Blackboard():

    def __init__(self) -> None:
        self.navigation_target = None
        self.navigation_status = None
        self.movement_speed = 0
        self.movement_factor = 0
        self.replan_requested = False

    def set_navigation_target(self, target):
        self.navigation_target = target

    def get_navigation_target(self):
        return self.navigation_target

    def set_navitation_status(self, status):
        self.navigation_status = status

    def get_navitation_status(self):
        return self.navigation_status

    def set_movement_speed(self, value):
        self.movement_speed = value

    def get_movement_speed(self):
        return self.movement_speed

    def set_movement_factor(self, value):
        self.movement_factor = value

    def get_movement_factor(self):
        return self.movement_factor

    def request_replan(self):
        self.replan_requested = True

    def is_replan_requested(self):
        return self.replan_requested
    
    
