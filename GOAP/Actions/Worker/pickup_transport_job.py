from GOAP.action import GOAPAction

class PickupTransportJob(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
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
        return True 

    def perform(self, agent):
        # perform the action
        if self.acquired_job:

            self.finished = True
            self.acquired_job.callback()
            
            return True

        if agent.owner.transport_queue.has_job():
            self.acquired_job = agent.owner.transport_queue.get_job()
            self.target = self.acquired_job.location

        return True