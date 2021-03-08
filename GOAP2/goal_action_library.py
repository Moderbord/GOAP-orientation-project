import game_time as time
from GOAP.transform import Position

from GOAP2.working_memory import FactType
from GOAP2.navigation_manager import NavStatus
from GOAP2.__goal import __Goal
from GOAP2.__action import __Action
from GOAP2.player import g_player

########## GOALS ##########
class g_CollectResource(__Goal):

    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"CollectResources" : True}

    def get_relevancy(self):
        return 0.5

class g_CollectOre(__Goal):

    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"CollectOre" : True}

    def get_relevancy(self):
        return 0.5

class g_CollectLogs(__Goal):

    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"CollectLogs" : True}

    def get_relevancy(self):
        return 0.7

########## ACTIONS ##########
class __a_GatherAction(__Action):
    def __init__(self) -> None:
        super().__init__()
        self.target_resource = None
        self.started_gathering = False
        self.gather_time = 5

    def activate(self, blackboard):
        blackboard.set_target_fact_type(FactType.Resource)
        blackboard.set_target_object_type(self.target_resource)

    def is_complete(self, blackboard):
        if self.started_gathering:
            blackboard.add_progress_time(time.clock.delta)
            if blackboard.get_progress_time() > self.gather_time:
                g_player.add_resource(self.target_resource)
                print("Gathered " + self.target_resource + "!")
                blackboard.reset_progress_time()
                self.started_gathering = False
                return True

        if blackboard.has_navigation_status(NavStatus.Arrived):
            self.started_gathering = True
            # remove memory fact?
        return False

class a_GatherOre(__a_GatherAction):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = "Ore"
        self.preconditions = {}
        self.effects = {"HasOre" : True, "HasResources" : True}
        self.cost = 10

class a_GatherLogs(__a_GatherAction):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = "Logs"
        self.preconditions = {}
        self.effects = {"HasLogs" : True, "HasResources" : True}
        self.cost = 5

class a_DeliverResources(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasResources" : True}
        self.effects = {"CollectResources" : True, "CollectOre" : True, "CollectLogs" : True}

    def activate(self, blackboard):
        blackboard.set_target_fact_type(FactType.Delivery)

    def is_complete(self, blackboard):
        if blackboard.has_navigation_status(NavStatus.Arrived):
            print("Deliver complete!")
            return True
        return False

class GoalActionLbrary():

    def __init__(self) -> None:
        goals = {}
        actions = {}
        
        #Goals
        goals["CollectResources"] = g_CollectResource()
        goals["CollectLogs"] = g_CollectLogs()
        goals["CollectOre"] = g_CollectOre()

        #Actions
        actions["GatherOre"] = a_GatherOre()
        actions["GatherLogs"] = a_GatherLogs()
        actions["DeliverResources"] = a_DeliverResources()

        # assign
        self.goals = goals
        self.actions = actions

    def load_goals(self, goals):
        return [self.goals.get(g) for g in goals]

    def load_actions(self, actions):
        return [self.actions.get(a) for a in actions]

g_galibrary = GoalActionLbrary()