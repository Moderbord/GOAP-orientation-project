from random import randint

import game_time as time
from game_server import g_map
from game_settings import g_prod
from GOAP.transform import Position
from GOAP.job_system import Job2, JobType

from GOAP2.__goal import __Goal
from GOAP2.__action import __Action
from GOAP2.navigation_manager import NavStatus
from GOAP2.working_memory import FactType, g_wmm
from GOAP2.blackboard import g_bbm
from GOAP2.player import g_player

# region --- GOALS ---

# region Units

class g_PerformJob(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"DoJob": True}


class g_UpgradeToArtisan(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"BecomeUpgraded": True}

    def get_relevancy(self, agent_id: int):
        return 1.0 if g_player.has_job(JobType.Upgrade, "Worker") else 0.0


class g_TransferResources(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"FetchedResource": True}

    def get_relevancy(self, agent_id: int):
        return 0.8 if g_player.has_job(JobType.Fetch) else 0.0


class g_FindResources(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"FindResources": True}

    def get_relevancy(self, agent_id: int):
        res = ["Logs", "Ore"]
        # knows atleast one of each resouce
        result = g_wmm.get_working_memory(agent_id).read_fact_type_where(
            FactType.Resource, lambda x: all([f in [v.object.value for v in x] for f in res]))
        return 0.1 if result else 0.6


class g_CollectResources(__Goal):

    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"CollectResource": True}

    def get_relevancy(self, agent_id: int):
        return 0.5

# endregion

# region Structures

class __g_ProductionGoal(__Goal):
    def get_relevancy(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        return 1.0 if bb.is_built() and bb.is_worked() else 0.0


class g_ProduceCoal(__g_ProductionGoal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"HasCoal": True}


class g_ProduceIronBar(__g_ProductionGoal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"HasIronBar": True}


class g_ProduceSword(__g_ProductionGoal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"HasSword": True}


class g_ProduceUnits(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"HasUnit": True}
    
    def get_relevancy(self, agent_id: int):
        return 0.3


class g_GetBuilt(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"IsBuilt": True}

    def get_relevancy(self, agent_id: int):
        # only relevant if not build
        return 0.0 if g_bbm.get_blackboard(agent_id).is_built() else 1.0


class g_GetWorked(__Goal):
    def __init__(self) -> None:
        super().__init__()
        self.goal_state = {"IsWorked": True}

    def get_relevancy(self, agent_id: int):
        # only relevant if not worked (will be placed after built due to priority)
        return 0.0 if g_bbm.get_blackboard(agent_id).is_worked() else 0.5

# endregion

# endregion


# region --- ACTIONS ---

# region Exploring

class a_Explore(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {}
        self.effects = {"FindResources": True, "Explore": True}
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
        return False  # TODO need to check working memory if agent has found resources


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

# endregion

# region Gathering

class __a_GatherAction(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = None
        self.gather_time = 5

    def is_valid(self, agent_id: int):
        # can be used to check if target tile still has required resource. Not ? -> remove fact and replan
        return super().is_valid(agent_id)

    def is_valid_in_context(self, agent_id: int):
        # agent must have a memory fact with the correct resource object
        return g_wmm.get_working_memory(agent_id).read_fact_type_where(FactType.Resource, lambda x: any([f.object.value == self.target_resource for f in x]))
        # return True

    def get_cost(self, agent_id: int):
        # should result in even gathering -> lower resource yields less cost
        return g_player.count_resource(self.target_resource)

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
            return False

        if blackboard.has_navigation_status(NavStatus.Arrived):
            pos = blackboard.get_position()
            tile = g_map.tile_data.get((pos.x, pos.y))
            if tile.deduct_resource_str(self.target_resource):
                blackboard.begin_timed_action()
                # pass  # TODO currently causes bug when workes freezes
                # successfully gonna gather resource
            else:
                g_wmm.get_working_memory(agent_id).delete_fact_where(FactType.Resource, lambda f: f.position.value == pos and f.object.value == self.target_resource)
                blackboard.set_request_replan(True)

        return False


class a_GatherOre(__a_GatherAction):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = "Ore"
        self.preconditions = {}
        self.effects = {"HasOre": True}
        self.cost = 10  # TODO override get_gost and count players current amount of resource


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
        self.effects = {"CollectLogs": True, "CollectResource": True}


class a_DeliverOre(__a_DeliverResourceAction):

    def __init__(self) -> None:
        super().__init__()
        self.target_resource = "Ore"
        self.preconditions = {"HasOre": True}
        self.effects = {"CollectOre": True, "CollectResource": True}

# endregion

# region Jobs

class a_DeliverResource(__Action):
    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasResource" : True}
        self.effects = {"FetchedResource" : True}

    def activate(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        job = bb.get_current_job()
        # structures blackboard
        target_bb = g_bbm.get_blackboard(job.sender_id)
        bb.set_manual_navigation_target(target_bb.get_position())
    
    def is_complete(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        if bb.has_navigation_status(NavStatus.Arrived):
            job = bb.get_current_job()
            target_bb = g_bbm.get_blackboard(job.sender_id)
            material = job.extra
            target_bb.inventory.append(material)
            print("Delivered " + material) # TODO append to target inventory
            bb.set_manual_navigation(False)
            return True

        return False

class a_PickupFetchJob(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.effects = {"HasResource": True}

    def is_valid_in_context(self, agent_id: int):
        return g_player.has_job(JobType.Fetch)

    def activate(self, agent_id: int):
        job = g_player.get_job(JobType.Fetch)
        bb = g_bbm.get_blackboard(agent_id)
        if job:
            bb.set_target_fact_type(FactType.Delivery)
            bb.set_current_job(job)
        else:
            bb.set_request_replan(True)

    def is_complete(self, agent_id: int):
        return g_bbm.get_blackboard(agent_id).has_navigation_status(NavStatus.Arrived)


class a_PickupUpgradeJob(__Action):

    def __init__(self) -> None:
        super().__init__()
        # TODO  Camp (which pickups and handles production job)
        self.effects = {"BecomeUpgraded": True}

    def is_valid_in_context(self, agent_id: int):
        return g_player.has_job(JobType.Upgrade, g_bbm.get_blackboard(agent_id).get_entity_str())

    def activate(self, agent_id: int):
        job = g_player.get_job(
            JobType.Upgrade, g_bbm.get_blackboard(agent_id).get_entity_str())
        bb = g_bbm.get_blackboard(agent_id)
        if job:
            bb.set_manual_navigation_target(job.location)
            bb.set_current_job(job)
        else:
            bb.set_request_replan(True)

    def is_complete(self, agent_id: int):
        # TODO destroy unit here?
        return g_bbm.get_blackboard(agent_id).has_navigation_status(NavStatus.Arrived)


class a_PickupBuildJob(__Action):
    def __init__(self) -> None:
        super().__init__()
        self.effects = {"HasJob": True}

    def is_valid_in_context(self, agent_id: int):
        # TODO and self.artisan == builder
        return g_player.has_job(JobType.Build)

    def activate(self, agent_id: int):
        job = g_player.get_job(JobType.Build)
        bb = g_bbm.get_blackboard(agent_id)
        if job:
            bb.set_manual_navigation_target(job.location)
            bb.set_current_job(job)
        else:
            bb.set_request_replan(True)

    def is_complete(self, agent_id: int):
        return g_bbm.get_blackboard(agent_id).has_navigation_status(NavStatus.Arrived)


class a_BuildStructure(__Action):
    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasJob": True}
        self.effects = {"DoJob": True}
        self.construction_time = 10  # TODO lookup

    def activate(self, agent_id: int):
        # g_bbm.get_blackboard(agent_id).begin_timed_action()
        pass

    def is_complete(self, agent_id: int):
        blackboard = g_bbm.get_blackboard(agent_id)
        blackboard.add_progress_time(time.clock.delta)

        if blackboard.get_progress_time() > self.construction_time:
            blackboard.reset_timed_progress()
            blackboard.set_manual_navigation(False)

            target_id = blackboard.get_current_job().sender_id
            g_bbm.get_blackboard(target_id).set_is_built(True)
            return True

        return False
# endregion

# region Structures

class a_CreateWorkJob(__Action):
    def __init__(self) -> None:
        super().__init__()
        self.effects = {"IsWorked": True}

    def activate(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        job = Job2(JobType.Work, agent_id, bb.get_position(), bb.get_required_artisan())
        g_player.add_job(job)

    def is_complete(self, agent_id: int):
        return g_bbm.get_blackboard(agent_id).is_worked()


class a_CreateBuildJob(__Action):
    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasMaterials" : True}
        self.effects = {"IsBuilt": True}

    def activate(self, agent_id: int):
        job = Job2(JobType.Build, agent_id, g_bbm.get_blackboard(agent_id).get_position())
        g_player.add_job(job)

    def is_complete(self, agent_id: int):
        return g_bbm.get_blackboard(agent_id).is_built()


class a_CreateFetchJob(__Action):
    def __init__(self) -> None:
        super().__init__()
        self.effects = {"HasMaterials": True}

    def activate(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        target = target = bb.get_production_target() if bb.is_built() else bb.get_entity_str()
        cost_table = g_prod[target]["CostTable"]
        bb.set_cost_table(cost_table)

        drop_off_loc = g_player.get_resource_drop_off_loc()
        for material, required_amount in cost_table.items():
            # current_amount = agent.inventory.count(material)
            # diff = max(required_amount - current_amount, 0)

            for x in range(0, required_amount):
                new_job = Job2(JobType.Fetch, agent_id, drop_off_loc, material)
                g_player.add_job(new_job)

    def is_complete(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        cost_table = bb.get_cost_table()

        if all([bb.inventory.count(key) >= cost_table.get(key) for key in cost_table.keys()]):
            print("materials received")
            return True
        return False


class a_PickupProductionJob(__Action):

    def __init__(self) -> None:
        super().__init__()
        self.effects = {"HasJob": True}

    def is_valid_in_context(self, agent_id: int):
        structure = g_bbm.get_blackboard(agent_id).get_entity_str()
        prod_list = g_prod[structure]["OutputTable"].keys()
        return g_player.has_job(JobType.Production, prod_list)

    def activate(self, agent_id: int):
        bb = g_bbm.get_blackboard(agent_id)
        structure = bb.get_entity_str()
        prod_list = g_prod[structure]["OutputTable"].keys()
        job = g_player.get_job(JobType.Production, prod_list)
        if job:
            bb.set_production_target(job.extra)
        else:
            bb.set_request_replan(True)

    def is_complete(self, agent_id: int):
        return True


class a_ProduceArtisan(__Action):
    def __init__(self) -> None:
        super().__init__()
        self.preconditions = {"HasMaterials" : True}
        self.effects = {"HasUnit" : True, "HasArtisan" : True}
        self.construction_time = g_prod["Artisan"]["ProductionTime"]
    
    def is_valid_in_context(self, agent_id: int):
        return g_bbm.get_blackboard(agent_id).get_production_target() == "Artisan"

    def activate(self, agent_id: int):
        # g_bbm.get_blackboard(agent_id).begin_timed_action()
        pass

    def is_complete(self, agent_id: int):
        blackboard = g_bbm.get_blackboard(agent_id)
        blackboard.add_progress_time(time.clock.delta)

        if blackboard.get_progress_time() > self.construction_time:
            blackboard.reset_timed_progress()
            print("Created artisan") # TODO add unit
            return True

        return False

# endregion


# endregion


class GoalActionLbrary():

    def __init__(self) -> None:
        goals = {}
        actions = {}

        # Goals
        goals["PerformJob"] = g_PerformJob()
        goals["UpgradeToArtisan"] = g_UpgradeToArtisan()
        goals["TransferResources"] = g_TransferResources()
        goals["CollectResources"] = g_CollectResources()
        goals["FindResources"] = g_FindResources()
        #
        goals["ProduceCoal"] = g_ProduceCoal()
        goals["ProduceIronBar"] = g_ProduceIronBar()
        goals["ProduceSword"] = g_ProduceSword()
        goals["ProduceUnits"] = g_ProduceUnits()
        goals["GetBuilt"] = g_GetBuilt()
        goals["GetWorked"] = g_GetWorked()

        # Actions
        actions["Explore"] = a_Explore()
        actions["FindLogs"] = a_FindLogs()
        actions["FindOre"] = a_FindOre()
        #
        actions["GatherLogs"] = a_GatherLogs()
        actions["GatherOre"] = a_GatherOre()
        actions["DeliverLogs"] = a_DeliverLogs()
        actions["DeliverOre"] = a_DeliverOre()
        #
        actions["DeliverResource"] = a_DeliverResource()
        actions["PickupFetchJob"] = a_PickupFetchJob()
        actions["PickupUpgradeJob"] = a_PickupUpgradeJob()
        actions["PickupBuildJob"] = a_PickupBuildJob()
        actions["BuildStructure"] = a_BuildStructure()
        #
        actions["CreateWorkJob"] = a_CreateWorkJob()
        actions["CreateBuildJob"] = a_CreateBuildJob()
        actions["CreateFetchJob"] = a_CreateFetchJob()
        actions["PickupProductionJob"] = a_PickupProductionJob()
        actions["ProduceArtisan"] = a_ProduceArtisan()

        # assign
        self.goals = goals
        self.actions = actions

    def load_goals(self, goals):
        return [self.goals.get(g) for g in goals]

    def load_actions(self, actions):
        return [self.actions.get(a) for a in actions]


g_galibrary = GoalActionLbrary()
