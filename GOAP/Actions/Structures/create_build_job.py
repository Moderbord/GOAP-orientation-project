from GOAP.action import GOAPAction
from GOAP.job_system import Job, JobType

class CreateBuildJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.requested_materials = False
        self.requested_builder = False

        # preconditions
        self.add_precondition("isBuilt", False)
        
        # effects
        self.add_effect("isBuilt", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False
        self.requested_materials = False
        self.requested_builder = False

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

        # need materials
        if not self.requested_materials:
            for material, required_amount in agent.construction_materials.items():
                current_amount = agent.raw_materials.count(material)
                diff = max(required_amount - current_amount, 0)

                for x in range(0, diff):
                    new_job = Job(JobType.Fetch, agent.position, material, agent.on_fetched)
                    agent.owner.add_job(new_job)

            self.requested_materials = True

        # then worker
        if not self.requested_builder and agent.has_materials:
            new_job = Job(JobType.Build, agent.position, agent.build_time, agent.on_built)
            agent.owner.add_job(new_job)
            self.requested_builder = True

        if agent.is_built:
            self.finished = True

        return True