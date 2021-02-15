import game_time as time

from GOAP.transform import Position
from GOAP.action import GOAPAction

class BuildStructure(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.target_structure = None
        self.progress = 0
        self.duration = 3

        # preconditions
        
        # effects
        self.add_effect("doJob", True)

    def reset(self):
        super().reset()
        # reset local state
        self.progress = 0
        self.finished = False

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        target_structure = agent.owner.get_structure_where(lambda x: not x.is_built)
        if target_structure:
            self.target_structure = target_structure
            self.target = target_structure.position
            return True

        return False 

    def perform(self, agent):
        # perform the action
        self.progress += time.clock.delta

        if self.progress >= self.duration:
            print(type(agent).__name__ + " done!")
            self.finished = True
            self.target_structure.on_built()
            agent.goal_state = None

        return True