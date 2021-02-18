from GOAP.action import GOAPAction
from GOAP.job_system import Job, JobType

class CreateWorkJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variable
        self.finished = False
        self.has_called = False

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("isWorked", False)
        
        # effects
        self.add_effect("isWorked", True)

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
            new_job = Job(JobType.Work, agent.position, agent.required_artisan, agent.on_worked)
            agent.owner.add_job(new_job)
            self.has_called = True

        if agent.is_worked:
            self.finished = True

        return True