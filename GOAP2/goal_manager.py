import game_time as time

from GOAP2.__manager import __Manager
from GOAP2.plan import Plan
from GOAP2.goap_planner import g_planner
from GOAP2.blackboard import g_bbm

class GoalManager(__Manager):

    def __init__(self, agent_id) -> None:
        super().__init__(agent_id)
        self.update_interval = 0 # currently depens on delta time every frame (if action does)
        self.plan = Plan()
        self.current_goal = None
        self.goal_map = {}
        self.world_state = {}
        self.actions = []

        self.replan_threshold = 5.0
        self.idle_time = 0.0

    def _update(self):
        blackboard = g_bbm.get_blackboard(self.agent_id)
        # update current goal
        if blackboard.is_replan_requested():
            blackboard.set_request_replan(False)

            self.update_goal_revelancies()
            # try every goal with a relevance greater than cero
            while any([val > 0.0 for val in self.goal_map.values()]):

                best_goal = self.find_most_relevant_goal()
                # reset relevance
                self.goal_map[best_goal] = 0.0 
                # get only actions that currently can be executed
                available_actions = [a for a in self.actions if a.is_valid_in_context(self.agent_id)]
                # build plan
                action_sequence = g_planner.build_plan(self.agent_id, best_goal.goal_state, self.world_state, available_actions)
                if action_sequence:
                    self.plan.set_action_plan(action_sequence)
                    self.plan.activate(self.agent_id)
                    self.current_goal = best_goal
                    break

        if self.plan.is_valid(self.agent_id):
            if self.plan.is_step_complete(self.agent_id):
                success = self.plan.advance(self.agent_id)
                if not success:
                    # all actions has been completed
                    #print("Plan completed!!")
                    blackboard.set_request_replan(True)
        
        else:
            self.idle_time += time.clock.delta
            if self.idle_time > self.replan_threshold:
                blackboard.set_request_replan(True)
                self.idle_time = 0
            pass
            # TODO replan?

    def update_goal_revelancies(self):
        for goal in self.goal_map.keys():
            self.goal_map[goal] = goal.get_relevancy(self.agent_id)

    def set_goals(self, goals):
        self.goal_map = {goal : 0.0 for goal in goals}

    def set_actions(self, actions):
        self.actions = actions

    def set_world_state(self, state):
        self.world_state = state

    def find_most_relevant_goal(self):
        return max(self.goal_map, key=self.goal_map.get)