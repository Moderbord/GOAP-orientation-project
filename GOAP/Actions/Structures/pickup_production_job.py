from GOAP.job_system import Job, JobType

from GOAP.action import GOAPAction

class PickupProductionJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.cost = 10
        
        # local variables
        self.finished = False

        # precondition
        self.add_precondition("isBuilt", True)

        # effects
        self.add_effect("doJob", True)

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
        # check for any required criterias for the action
        return agent.owner.has_job(JobType.Production, agent.production_table.keys())

    def perform(self, agent):
        # perform the action
        job = agent.owner.get_job(JobType.Production, agent.production_table.keys())
        if job:
            agent.production_target = job.extra
            agent.on_resource_change()
            self.finished = True
            return True
        
        return False
