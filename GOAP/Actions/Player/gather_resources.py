from GOAP.action import GOAPAction
from GOAP.action_set import ActionSet

class GatherResources(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False

        # preconditions
        
        # effects
        self.add_effect("gatherResources", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False

    def requires_in_range(self):
        # does action require agent to be in range
        return False

    # def get_cost(self):
    #     # returns the intrinsic cost of the action
    #     return self.cost

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        return True

    def perform(self, agent):
        # perform the action
        maximun_gatherers = 5
        gather_table = {}
        #gathering_types = ["collectOre", "collectLogs"]
        gathering_types = ["collect" + s for s in ["Ore", "Logs"]] # ÓwÒ

        all_workers = agent.get_units("Worker")
        idle_workers = [e for e in all_workers if e.goal_state is None] # worker is idle

        if not idle_workers: # no idle workers -> skip
            self.finished = True
            return True

        for gather_type in gathering_types:
            gather_table[gather_type] = len([e for e in all_workers if not e.goal_state is None and e.goal_state.get(gather_type)]) # construct initial gathering table
        
        current_gatherers = sum(gather_table.values())
        diff = min(maximun_gatherers - current_gatherers, len(idle_workers)) # get potential number of gatherers or minimun available workers

        for i in range(diff):      
            least_gathered = min(gather_table, key=gather_table.get) # get the least gathered resource <-- this defines the gathering behavior

            goal_state = ActionSet()
            goal_state.add(least_gathered, True)
            idle_workers[i].set_goal_state(goal_state) # check if locked from gathering?

            gather_table[least_gathered] = gather_table.get(least_gathered) + 1
            current_gatherers += 1

        if current_gatherers >= maximun_gatherers:
            self.finished = True

        return True