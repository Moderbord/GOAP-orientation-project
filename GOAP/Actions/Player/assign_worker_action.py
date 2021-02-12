from GOAP.action import GOAPAction
from GOAP.action_set import ActionSet

class AssignWorkerAction(GOAPAction):

    def __init__(self):
        super().__init__()
        # loval variables
        self.finished = False
        self.target_worker = None
        self.target_command = None

        # preconditions
        self.add_precondition("hasFreeWorker", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False

    def requires_in_range(self):
        # does action require agent to be in range
        return False

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # get free worker
        workers = agent.get_units("Worker")
        for worker in workers:
            if not worker.goal_state: # has no set goal

                goal_state = ActionSet()
                goal_state.add("recievingPlan", True)
                worker.goal_state = goal_state

                self.target_worker = worker
                break

        return True

    def perform(self, agent):
        # didn't get free worker
        if not self.target_worker:
            return False

        # perform the action
        goal_state = ActionSet()
        goal_state.add(self.target_command, True)
        self.target_worker.set_goal_state(goal_state)
        self.finished = True
        
        #agent.resolve_goal(self.effects)

        return True