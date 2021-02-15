from random import randint

from GOAP.transform import Position
from GOAP.action import GOAPAction

class Explore(GOAPAction):

    def __init__(self):
        super().__init__()
        self.finished = False

        # local variables

        # preconditions
        
        # effects
        self.add_effect("isExploring", True)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        self.target = self.__get_new_position()
        return True

    def perform(self, agent):
        # perform the action
        self.target = self.__get_new_position()
        self.in_range = False
        return True

    def __get_new_position(self):
        return Position(randint(1, 50), randint(1, 50))