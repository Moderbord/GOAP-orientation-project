from GOAP2.__goal import __Goal
from GOAP2.__action import __Action

class g_CollectResource(__Goal):

    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"CollectResources" : True}

    def update_relevance(self):
        self.relevancy = 0.5

class a_GatherBerries(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {}
        # self.preconditions = {"HasResources" : False}
        self.effects = {"HasResources" : True}
        self.cost = 10

class a_GatherLogs(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasTools" : True}
        # self.preconditions = {"HasResources" : False, "HasTools" : True}
        self.effects = {"HasResources" : True}
        self.cost = 5

class a_GetTools(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"ToolsAvailable" : True}
        self.effects = {"HasTools" : True}

class a_DeliverResources(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasResources" : True}
        self.effects = {"CollectResources" : True}


class GoalActionLbrary():

    def __init__(self) -> None:
        goals = {}
        actions = {}
        
        #Goals
        goals["CollectResources"] = g_CollectResource()

        #Actions
        actions["GatherBerries"] = a_GatherBerries()
        actions["GatherLogs"] = a_GatherLogs()
        actions["GetTools"] = a_GetTools()
        actions["DeliverResources"] = a_DeliverResources()

        # assign
        self.goals = goals
        self.actions = actions

    def load_goals(self, goals):
        goal_set = []
        for g in goals:
            goal_set.append(self.goals.get(g))
        return goal_set

    def load_actions(self, actions):
        action_set = []
        for a in actions:
            action_set.append(self.actions.get(a))
        return action_set

g_galibrary = GoalActionLbrary()