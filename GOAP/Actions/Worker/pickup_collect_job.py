from GOAP.job_system import JobType

from GOAP.action import GOAPAction

class PickupCollectJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.cost = 5

        # local variables
        self.finished = False
        self.collected_item = False
        self.acquired_job = None
        self.progress = 0

        # preconditions
        #self.add_precondition("isBuilder", True)
        # effects
        self.add_effect("doJob", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False
        self.collected_item = False
        self.acquired_job = None
        self.progress = 0

    def requires_in_range(self):
        # does action require agent to be in range
        return True if self.acquired_job else False

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        return agent.owner.has_job(JobType.Collect)

    def perform(self, agent):
        # perform the action

        # dropoff location
        if self.collected_item:
            agent.owner.resources.append(self.acquired_job.extra)
            agent.backpack.remove(self.acquired_job.extra)
            self.finished = True
            return True

        # pickup location
        if self.acquired_job:
            # reset 
            self.in_range = False

            if self.acquired_job.callback():    # successfully collects item
                agent.backpack.append(self.acquired_job.extra)
                self.target = agent.owner.get_resource_drop_off_loc()
                self.collected_item = True
                return True
            
            return False # plan fails

        # get job
        job = agent.owner.get_job(JobType.Collect)
        if job:
            self.target = job.location
            self.acquired_job = job
            return True

        return False