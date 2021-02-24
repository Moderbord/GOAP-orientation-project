import game_time as time

from GOAP.action import GOAPAction
from GOAP.job_system import Job, JobType

class ProduceUnit(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.is_producing = False
        self.requested_unit = False
        self.progress = 0

        # refs
        self.agent_position = None
        self.add_player_unit = None

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False
        self.is_producing = False
        self.requested_unit = False
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

    def on_start(self, agent):
        super().on_start(agent)
        self.agent_position = agent.position
        self.add_player_unit = agent.owner.add_unit

    def perform(self, agent):
        # perform the action

        # produce
        if self.is_producing:
            self.progress += time.clock.delta

            if self.progress >= self.production_time:
                #print(type(agent).__name__ + " " + self.message_on_finish)
                self.on_production_finish()
                # reset
                agent.on_resource_change()
                agent.production_target = "" 
                agent.production_ready = False
                
                self.finished = True

            return True

        # wait for materials
        if not agent.has_materials:
            return True

        # wait for precursor unit
        if self.precursor_unit:
            # send for unit
            if not self.requested_unit:
                new_job = Job(JobType.Upgrade, agent.position, self.precursor_unit, agent.on_production_begin)
                agent.owner.add_job(new_job)
                self.requested_unit = True
            # unit arrived
            if agent.production_ready:
                self.is_producing = True

        else: # no precursor -> start production
            agent.on_production_begin()
            self.is_producing = True

        return True