from GOAP2.plan import Plan
from GOAP2.__manager import __Manager
from GOAP2.goap_planner import g_planner

class GoalManager(__Manager):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 0 # currently depens on delta time every frame (if action does)
        self.plan = Plan()
        self.current_goal = None
        self.goal_map = {}
        self.world_state = {}
        self.actions = []

    def _update(self):
        # update current goal
        if self.blackboard.is_replan_requested():
            self.blackboard.set_request_replan(False)

            self.update_goal_revelancies()
            # try every goal with a relevance greater than cero
            while any([val > 0.0 for val in self.goal_map.values()]):

                best_goal = self.find_most_relevant_goal()
                # reset relevance
                self.goal_map[best_goal] = 0.0 
                # get only actions that currently can be executed
                available_actions = [a for a in self.actions if a.is_valid_in_context(self.working_memory)]
                # build plan
                action_sequence = g_planner.build_plan(best_goal.goal_state, self.world_state, available_actions)
                if action_sequence:
                    self.plan.set_action_plan(action_sequence)
                    self.plan.activate(self.blackboard)
                    self.current_goal = best_goal
                    break

        if self.plan.is_valid(self.blackboard):
            if self.plan.is_step_complete(self.blackboard):
                success = self.plan.advance(self.blackboard)
                if not success:
                    # all actions has been completed
                    print("Plan completed!!")
                    self.blackboard.set_request_replan(True)
        
        else:
            pass
            # TODO replan?

    def update_goal_revelancies(self):
        for goal in self.goal_map.keys():
            self.goal_map[goal] = goal.get_relevancy()

    def set_goals(self, goals):
        self.goal_map = {goal : 0.0 for goal in goals}

    def set_actions(self, actions):
        self.actions = actions

    def set_world_state(self, state):
        self.world_state = state

    def find_most_relevant_goal(self):
        return max(self.goal_map, key=self.goal_map.get)