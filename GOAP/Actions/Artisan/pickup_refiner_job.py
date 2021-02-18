from GOAP.action import GOAPAction
from GOAP.job_system import JobType
from GOAP.Agents.artisan import Profession

class PickupRefinerJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.acquired_job = None

        # preconditions
        self.add_precondition("isRefiner", True)
        # effects
        self.add_effect("doJob", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False
        # self.acquired_job = None

    def requires_in_range(self):
        # does action require agent to be in range
        return True if self.acquired_job else False

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        # stays at first job acquired
        return agent.owner.has_job(JobType.Work, Profession.Refiner)

    def perform(self, agent):
        # perform the action 
        if self.acquired_job:
            self.finished = True
            self.acquired_job.callback()
            return True

        job = agent.owner.get_job(JobType.Work, Profession.Refiner)
        if job:
            self.target = job.location
            self.acquired_job = job

        return True