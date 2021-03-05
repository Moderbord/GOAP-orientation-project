from GOAP.transform import Position

from GOAP2.working_memory import FactType
from GOAP2.navigation_manager import NavStatus
from GOAP2.__goal import __Goal
from GOAP2.__action import __Action

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
class a_GatherOre(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {}
        self.effects = {"HasOre" : True, "HasResources" : True}
        self.cost = 10

    def activate(self, blackboard):
        blackboard.set_target_fact_type(FactType.Resource)
        blackboard.set_target_object_type("Ore")

    def is_complete(self, blackboard):
        return blackboard.has_object("Ore")


class a_GatherLogs(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {}
        self.effects = {"HasLogs" : True, "HasResources" : True}
        self.cost = 5

    def activate(self, blackboard):
        blackboard.set_target_fact_type(FactType.Resource)
        blackboard.set_target_object_type("Logs")

    def is_complete(self, blackboard):
        # return blackboard.has_object("Logs")
        if blackboard.has_navigation_status(NavStatus.Arrived):
            print("Gather logs complete!")
            return True
        return False

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