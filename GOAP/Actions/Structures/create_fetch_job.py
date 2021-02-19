from random import randint
from GOAP.action import GOAPAction
from GOAP.job_system import Job, JobType

class CreateFetchJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("hasMaterials", False)
        
        # effects
        self.add_effect("hasMaterials", True)

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
        return True

    def perform(self, agent):
        # perform the action
        for material, required_amount in agent.production_target_requirements.items():
            current_amount = agent.raw_materials.count(material)
            diff = max(required_amount - current_amount, 0)

            for x in range(0, diff):
                new_job = Job(JobType.Fetch, agent.position, material, agent.on_fetched)
                agent.owner.add_job(new_job)

        self.finished = True

        return True