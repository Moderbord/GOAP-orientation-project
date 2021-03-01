from GOAP2.sensor_manager import SensorManager
from GOAP2.navigation_manager import NavigationManager
from GOAP2.target_manager import TargetManager
from GOAP2.blackboard import Blackboard
from GOAP2.working_memory import WorkingMemory
from GOAP2.__entity import __Entity



class GOAPController():

    def __init__(self) -> None:
        # AI module
        self.sensor_mgr = None
        self.target_mgr = None
        self.navigation_mgr = None
        self.blackboard = None
        self.entity = None
        self.working_memory = None
        # GOAP
        self.goal_mgr = None
        self.action_set = None
        self.current_world_states = None
        self.plan = None

    def setup(self, entity, blackboard):
        self.entity = entity
        
        blackboard.set_position(entity.position)
        self.blackboard = blackboard

        self.navigation_mgr.set_blackboard(self.blackboard)

    def enable_navigation(self):
        self.navigation_mgr = NavigationManager()
    
    def update(self):
        # Check if agent has moved
        if self.blackboard.has_new_position():
            self.entity.set_position(self.blackboard.get_position())
            self.blackboard.new_position_notified()

        self.entity.update()
        self.navigation_mgr.update()

    

