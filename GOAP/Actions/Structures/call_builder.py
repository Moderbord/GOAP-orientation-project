from GOAP.action import GOAPAction
from GOAP.action_set import ActionSet
from GOAP.Agents.artisan import Profession

class CallBuilder(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.finished = False

        # local variables
        self.target_builder = None

        # preconditions
        self.add_precondition("isBuilt", False)
        
        # effects
        self.add_effect("isBuilt", True)

    def reset(self):
        super().reset()
        # reset local state
        self.target_builder = None

    def requires_in_range(self):
        # does action require agent to be in range
        return False

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        builders = agent.owner.get_unit_type_where("Artisan", lambda x: x.profession is Profession.Builder)
        for builder in builders:
            if builder.goal_state is None: # builder is idle

                goal_state = ActionSet()
                goal_state.add("doJob", True)
                builder.set_goal_state(goal_state)

                self.target_builder = builder
                print("found")
                break

        return True if self.target_builder else False

    def perform(self, agent):
        # perform the action
        if agent.is_built:
            self.finished = True

        return True