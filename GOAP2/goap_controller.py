from GOAP2.sensor_manager import SensorManager
from GOAP2.navigation_manager import NavigationManager
from GOAP2.target_manager import TargetManager
from GOAP2.blackboard import Blackboard
from GOAP2.agent import Agent
from GOAP2.working_memory import WorkingMemory



class GOAPController():

    def __init__(self) -> None:
        # AI module
        self.sensor_mgr = None
        self.navigation_mgr = None
        self.target_mgr = None
        self.blackboard = None
        self.agent = None
        self.working_memory = None
        # GOAP
        self.goal_mgr = None
        self.action_set = None
        self.current_world_states = None
        self.plan = None
        
        # self.sensor_mgr = SensorManager()
        # self.navigation_mgr = NavigationManager()
        # self.target_mgr = TargetManager()
        # self.blackboard = Blackboard()
        # self.agent = Agent()
        # self.working_memory = WorkingMemory()

    def setup(self):
        pass
    
    def update(self):
        pass

    

