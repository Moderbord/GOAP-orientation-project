from GOAP.action import GOAPAction
from GOAP.job_system import JobType
from GOAP.Agents.artisan import Profession

class PickupMetallurgistJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.acquired_job = None

        # preconditions
        self.add_precondition("isMetallurgist", True)
        # effects
        self.add_effect("doJob", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False

    def requires_in_range(self):
        # does action require agent to be in range
        return True if self.acquired_job else False

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        # stays at first job acquired
        job_found = agent.owner.has_job(JobType.Work, Profession.Metallurgist)

        if agent.profession is None and job_found:
            agent.profession = Profession.Metallurgist

        return job_found

    def perform(self, agent):
        # perform the action 
        if self.acquired_job:
            self.finished = True
            self.acquired_job.callback()
            return True

        job = agent.owner.get_job(JobType.Work, Profession.Metallurgist)
        if job:
            self.target = job.location
            self.acquired_job = job

        return True