from math import gamma
from random import randint

import game_time as time
from game_server import g_map
from GOAP.transform import Position

from GOAP2.__goal import __Goal
from GOAP2.__action import __Action
from GOAP2.navigation_manager import NavStatus
from GOAP2.working_memory import FactType, g_wmm
from GOAP2.blackboard import g_bbm
from GOAP2.player import g_player

# region --- GOALS ---


class g_FindResources(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"FindResources": True}

    def get_relevancy(self, agent_id: int):
        res = ["Logs", "Ore"]
        # knows atleast one of each resouce
        result = g_wmm.get_working_memory(agent_id).read_fact_type_where(FactType.Resource, lambda x: all([f in [v.object.value for v in x] for f in res]))
        return 0.1 if result else 0.6

class g_CollectResources(__Goal):

    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"CollectResources": True}

    def get_relevancy(self, agent_id: int):
        return 0.5
# endregion


# region --- ACTIONS ---

class a_Explore(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {}
        self.effects = {"FindResources": True, "Explore" : True}
        self.target_resource = None
    
    def activate(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        radius = 50
        pos = (0, 0)
        while pos in g_map.unpassable_tiles:
            pos = (randint(1, radius), randint(1, radius))
        bb.set_manual_navigation_target(Position(pos[0], pos[1]))

    def is_complete(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        # check if target resource has been found
        if self.target_resource:
            if g_wmm.get_working_memory(agent_id).read_fact_type_where(FactType.Resource, lambda x: any([f.object.value == self.target_resource for f in x])):
                bb.set_manual_navigation(False)
                return True

        if bb.has_navigation_status(NavStatus.Arrived):
            bb.set_manual_navigation(False)
            return True
        return False # TODO need to check working memory if agent has found resources
        
class a_FindLogs(a_Explore):
    def __init__(self) -> None:
        super().__init__()
        #self.effects = {"FindLogs": True}
        self.target_resource = "Logs"

    def get_cost(self, agent_id: int):
        return g_wmm.get_working_memory(agent_id).read_fact_type_where(FactType.Resource, lambda x: len([f for f in x if f.object.value == self.target_resource]))

class a_FindOre(a_Explore):
    def __init__(self) -> None:
        super().__init__()
        #self.effects = {"FindOre": True}
        self.target_resource = "Ore"

    def get_cost(self, agent_id: int):
        return g_wmm.get_working_memory(agent_id).read_fact_type_where(FactType.Resource, lambda x: len([f for f in x if f.object.value == self.target_resource]))


# region Gathering

class __a_GatherAction(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = None
        self.gather_time = 5

    def is_valid_in_context(self, agent_id: int):
        # agent must have a memory fact with the correct resource object
        return g_wmm.get_working_memory(agent_id).read_fact_type_where(FactType.Resource, lambda x: any([f.object.value == self.target_resource for f in x]))
        #return True

    def get_cost(self, agent_id: int):
        return g_player.count_resource(self.target_resource) # should result in even gathering -> lower resource yields less cost

    def activate(self, agent_id: int):
        blackboard = g_bbm.get_blackboard(agent_id)
        blackboard.set_target_fact_type(FactType.Resource)
        blackboard.set_targeting_function(lambda x: max([p for p in [f for f in x if f.object.value == self.target_resource]], key=lambda c: c.position.confidence, default=None))

    def is_complete(self, agent_id: int):
        blackboard = g_bbm.get_blackboard(agent_id)
        if blackboard.began_timed_action():
            blackboard.add_progress_time(time.clock.delta)
            if blackboard.get_progress_time() > self.gather_time:
                blackboard.reset_timed_progress()
                print("Gathered " + self.target_resource + "!")
                # TODO remove memory fact? <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                return True

        if blackboard.has_navigation_status(NavStatus.Arrived):
            pos = blackboard.get_position()
            tile = g_map.tile_data.get((pos.x, pos.y))
            if tile.deduct_resource_str(self.target_resource):
                pass #TODO currently causes bug when workes freezes
                # successfully gonna gather resource
            blackboard.begin_timed_action()
            # else:
            #     g_wmm.get_working_memory(agent_id).delete_fact_where(FactType.Resource, lambda f: f.position.value == pos)
            #     blackboard.set_request_replan(True)
        
        return False


class a_GatherOre(__a_GatherAction):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = "Ore"
        self.preconditions = {}
        self.effects = {"HasOre": True}
        self.cost = 10 # TODO override get_gost and count players current amount of resource


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
        self.target_resource = None
        self.preconditions = {}
        self.effects = {}

    def activate(self, agent_id: int):
        g_bbm.get_blackboard(agent_id).set_target_fact_type(FactType.Delivery)

    def is_complete(self, agent_id: int):
        if g_bbm.get_blackboard(agent_id).has_navigation_status(NavStatus.Arrived):
            g_player.add_resource(self.target_resource)
            #print("Deliver complete!")
            return True
        return False


class a_DeliverLogs(__a_DeliverResourceAction):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = "Logs"
        self.preconditions = {"HasLogs": True}
        self.effects = {"CollectLogs": True, "CollectResources": True}

class a_DeliverOre(__a_DeliverResourceAction):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = "Ore"
        self.preconditions = {"HasOre": True}
        self.effects = {"CollectOre": True, "CollectResources": True}

# endregion

# endregion


class GoalActionLbrary():

    def __init__(self) -> None:
        goals = {}
        actions = {}

        # Goals
        goals["CollectResources"] = g_CollectResources()
        goals["FindResources"] = g_FindResources()
        # goals["CollectLogs"] = g_CollectLogs()
        # goals["CollectOre"] = g_CollectOre()

        # Actions
        actions["GatherOre"] = a_GatherOre()
        actions["GatherLogs"] = a_GatherLogs()
        actions["DeliverLogs"] = a_DeliverLogs()
        actions["DeliverOre"] = a_DeliverOre()
        actions["Explore"] = a_Explore()
        actions["FindLogs"] = a_FindLogs()
        actions["FindOre"] = a_FindOre()

        # assign
        self.goals = goals
        self.actions = actions

    def load_goals(self, goals):
        return [self.goals.get(g) for g in goals]

    def load_actions(self, actions):
        return [self.actions.get(a) for a in actions]


g_galibrary = GoalActionLbrary()
