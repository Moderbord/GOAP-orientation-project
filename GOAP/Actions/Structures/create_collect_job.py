from GOAP.action import GOAPAction
from GOAP.job_system import Job, JobType

class CreateCollectJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        self.finished = False

        # local variables

        # preconditions
        self.add_precondition("hasProduce", True)
        
        # effects
        self.add_effect("supplyProduce", True)

    def reset(self):
        super().reset()
        # reset local state

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
        new_job = Job(JobType.Collect, agent.position, agent.produced_material, agent.on_collect)
        agent.owner.transport_queue.append(new_job)

        self.finished = True

        return True