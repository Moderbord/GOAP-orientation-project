from GOAP.action import GOAPAction
from GOAP.job_system import Job, JobType

class CreateBuildJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.has_called = False

        # preconditions
        self.add_precondition("isBuilt", False)
        
        # effects
        self.add_effect("isBuilt", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False
        self.has_called = False

    def requires_in_range(self):
        # does action require agent to be in range
        return False

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        return True

    def perform(self, agent):
        # perform the action
        if not self.has_called:
            new_job = Job(JobType.Build, agent.position, agent.build_time, agent.on_built)
            agent.owner.add_job(new_job)
            self.has_called = True

        if agent.is_built:
            self.finished = True

        return True