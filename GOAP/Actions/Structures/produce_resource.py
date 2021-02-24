import game_time as time

from GOAP.action import GOAPAction
from GOAP.job_system import Job, JobType

class ProduceResource(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.is_producing = False
        self.progress = 0

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False
        self.is_producing = False
        self.progress = 0

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
        if agent.production_ready:
            self.progress += time.clock.delta

            if self.progress >= self.production_time:
                #print(type(agent).__name__ + " " + self.message_on_finish)
                agent.produce.append(self.target_resource)
                self.finished = True

                # create pickup job
                new_job = Job(JobType.Collect, agent.position, self.target_resource, agent.on_collected)
                agent.owner.add_job(new_job)

            return True

        if agent.has_materials:
            agent.on_production_begin()
            agent.inventory_update()
            self.is_producing = True

        return True