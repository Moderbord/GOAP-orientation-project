import game_time as time

from GOAP.action import GOAPAction
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
        self.acquired_job = None

    def requires_in_range(self):
        # does action require agent to be in range
        return True if self.acquired_job else False

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        return True 

    def perform(self, agent):
        # perform the action 
        if self.acquired_job:
            self.finished = True
            self.acquired_job.callback()
            return True

        if agent.owner.work_queue.has_job():
            job = agent.owner.work_queue.get_job()
            # acquired_job.extra -> profession
            if not job.extra == Profession.Refiner:
                agent.owner.work_queue.append(job) # suuuuuuuuuuper slim chance of soft-locking should two artisans compete to get respective jobs
                return True
            
            self.target = job.location
            self.acquired_job = job

        return True