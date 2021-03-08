from GOAP2.sensor_manager import SensorManager
from GOAP2.navigation_manager import NavigationManager
from GOAP2.target_manager import TargetManager
from GOAP2.goal_manager import GoalManager
from GOAP2.__entity import __Entity

from GOAP2.blackboard import g_bbm
from GOAP2.working_memory import g_wmm
from GOAP2.goal_action_library import g_galibrary


class GOAPController():

    id_count = 0

    def __init__(self) -> None:
        self.id = GOAPController.id_count
        # AI module
        self.sensor_mgr = None
        self.target_mgr = None
        self.navigation_mgr = None
        self.blackboard = None
        self.entity = None
        self.working_memory = None
        # GOAP
        self.goal_mgr = None
        # increment
        GOAPController.id_count += 1

    def setup(self, entity):
        self.entity = entity
        # blackboard
        self.blackboard = g_bbm.create_blackboard(self.id)
        self.blackboard.set_position(entity.position)
        # working memory
        self.working_memory = g_wmm.create_working_memory(self.id)
        # GOAP
        self.goal_mgr = GoalManager(self.id)
        self.goal_mgr.set_goals(g_galibrary.load_goals(entity.goals))
        self.goal_mgr.set_actions(g_galibrary.load_actions(entity.available_actions))
        self.goal_mgr.set_world_state(entity.world_state)
       
    def enable_navigation(self):
        self.navigation_mgr = NavigationManager(self.id)

    def enable_targeting(self):
        self.target_mgr = TargetManager(self.id)

    def enable_sensors(self):
        self.sensor_mgr = SensorManager(self.id)
    
    def attach_sensor(self, sensor):
        if not self.sensor_mgr:
            self.sensor_mgr = SensorManager(self.id)
        self.sensor_mgr.add_sensor(sensor)
    
    def update(self):
        # Check if agent has moved
        if self.blackboard.has_new_position():
            self.entity.set_position(self.blackboard.get_position())
            self.blackboard.new_position_notified()

        if self.sensor_mgr:
            self.sensor_mgr.update()
        if self.target_mgr:
            self.target_mgr.update()
        if self.navigation_mgr:
            self.navigation_mgr.update()
        self.goal_mgr.update()
        self.entity.update()

    

