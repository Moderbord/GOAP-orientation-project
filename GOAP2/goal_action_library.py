from random import randint

import game_time as time
from GOAP.transform import Position

from GOAP2.__goal import __Goal
from GOAP2.__action import __Action
from GOAP2.navigation_manager import NavStatus
from GOAP2.working_memory import WorkingMemory, FactType, g_wmm
from GOAP2.blackboard import g_bbm
from GOAP2.player import g_player

# region --- GOALS ---


class g_FindResources(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"FindResources": True}

    def get_relevancy(self, agent_id: int):
        return 0.1


class g_CollectOre(__Goal):

    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"CollectOre": True}

    def get_relevancy(self, agent_id: int):
        return 0.5


class g_CollectLogs(__Goal):

    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"CollectLogs": True}

    def get_relevancy(self, agent_id: int):
        return 0.7
# endregion


# region --- ACTIONS ---

class a_Explore(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {}
        self.effects = {"FindResources": True}
    
    def activate(self, agent_id: int):
        pass

    def is_complete(self, agent_id: int):
        return True # TODO need to check working memory if agent has found resources
        


# region Gathering

class __a_GatherAction(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = None
        self.started_gathering = False
        self.gather_time = 5

    def is_valid_in_context(self, agent_id: int):
        # agent must have a memory fact with the correct resource object
        return g_wmm.get_working_memory(agent_id).read_fact_type_where(FactType.Resource, lambda x: any([f.object.value == self.target_resource for f in x]))
        #return True

    def activate(self, agent_id: int):
        blackboard = g_bbm.get_blackboard(agent_id)
        blackboard.set_target_fact_type(FactType.Resource)
        blackboard.set_target_object_type(self.target_resource)

    def is_complete(self, agent_id: int):
        blackboard = g_bbm.get_blackboard(agent_id)
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
        self.effects = {"HasOre": True}
        self.cost = 10


class a_GatherLogs(__a_GatherAction):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = "Logs"
        self.preconditions = {}
        self.effects = {"HasLogs": True}
        self.cost = 5


class __a_DeliverResourceAction(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {}
        self.effects = {}

    # def activate(self):
    #     blackboard.set_target_fact_type(FactType.Delivery)

    def is_complete(self, agent_id: int):
        if g_bbm.get_blackboard(agent_id).has_navigation_status(NavStatus.Arrived):
            print("Deliver complete!")
            return True
        return False


class a_DeliverLogs(__a_DeliverResourceAction):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasLogs": True}
        self.effects = {"CollectLogs": True}

    def activate(self, agent_id: int):
        g_bbm.get_blackboard(agent_id).set_target_fact_type(FactType.Delivery)

class a_DeliverOre(__a_DeliverResourceAction):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasOre": True}
        self.effects = {"CollectOre": True}

    def activate(self, agent_id: int):
        g_bbm.get_blackboard(agent_id).set_target_fact_type(FactType.Delivery)

# endregion

# endregion


class GoalActionLbrary():

    def __init__(self) -> None:
        goals = {}
        actions = {}

        # Goals
        goals["FindResources"] = g_FindResources()
        goals["CollectLogs"] = g_CollectLogs()
        goals["CollectOre"] = g_CollectOre()

        # Actions
        actions["GatherOre"] = a_GatherOre()
        actions["GatherLogs"] = a_GatherLogs()
        actions["DeliverLogs"] = a_DeliverLogs()
        actions["DeliverOre"] = a_DeliverOre()
        actions["Explore"] = a_Explore()

        # assign
        self.goals = goals
        self.actions = actions

    def load_goals(self, goals):
        return [self.goals.get(g) for g in goals]

    def load_actions(self, actions):
        return [self.actions.get(a) for a in actions]


g_galibrary = GoalActionLbrary()
