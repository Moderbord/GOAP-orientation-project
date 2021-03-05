from GOAP2.sensor_manager import SensorManager
from GOAP2.navigation_manager import NavigationManager
from GOAP2.target_manager import TargetManager
from GOAP2.blackboard import Blackboard
from GOAP2.working_memory import WorkingMemory
from GOAP2.goal_manager import GoalManager
from GOAP2.__entity import __Entity

from GOAP2.goal_action_library import g_galibrary


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

    def setup(self, entity, blackboard):
        self.entity = entity
        # blackboard
        blackboard.set_position(entity.position)
        self.blackboard = blackboard
        # working memory
        self.working_memory = WorkingMemory()
        # sensors
        if self.sensor_mgr:
            self.sensor_mgr.set_blackboard(self.blackboard)
            self.sensor_mgr.set_working_memory(self.working_memory)
        # navigation
        if self.navigation_mgr:
            self.navigation_mgr.set_blackboard(self.blackboard)
        # targeting
        if self.target_mgr:
            self.target_mgr.set_blackboard(self.blackboard)
            self.target_mgr.set_working_memory(self.working_memory)

        # GOAP
        self.goal_mgr = GoalManager()
        self.goal_mgr.set_blackboard(self.blackboard)
        self.goal_mgr.set_goals(g_galibrary.load_goals(entity.goals))
        self.goal_mgr.set_actions(g_galibrary.load_actions(entity.available_actions))
        self.goal_mgr.set_world_state(entity.world_state)
       
    def enable_navigation(self):
        self.navigation_mgr = NavigationManager()

    def enable_targeting(self):
        self.target_mgr = TargetManager()

    def enable_sensors(self):
        self.sensor_mgr = SensorManager()
    
    def update(self):
        # Check if agent has moved
        if self.blackboard.has_new_position():
            self.entity.set_position(self.blackboard.get_position())
            self.blackboard.new_position_notified()

        self.sensor_mgr.update()
        self.target_mgr.update()
        self.navigation_mgr.update()
        self.goal_mgr.update()
        self.entity.update()

    

