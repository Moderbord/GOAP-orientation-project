from random import randint

from game_server import g_map

from GOAP.action import GOAPAction
from GOAP.transform import Position
from GOAP.transform import distance

class SurveyTerritory(GOAPAction):

    def __init__(self):
        super().__init__()
        # overrides
        # self.target = None
        # self.in_range = False
        # self.minimun_range = 0
        self.cost = 45.0

        # loval variables
        self.finished = False
        self.area = 25
        self.points_visited = 0
        self.survey_points = 0

        # preconditions
        self.add_precondition("isLonely", True)
        self.add_precondition("isBored", True)
        
        # effects
        self.add_effect("staySatisfied", True)
        self.add_effect("isHome", False)

    def reset(self):
        super().reset()
        # reset local state
        self.finished = False
        self.points_visited = 0
        self.survey_points = 0

    def requires_in_range(self):
        # does action require agent to be in range
        return True

    # def get_cost(self):
    #     # returns the intrinsic cost of the action
    #     return self.cost

    def completed(self):
        # is action completed
        return self.finished

    def check_precondition(self, agent):
        # check for any required criterias for the action
        self.target = self.__get_new_position()
        return True

    def on_start(self, agent):
        super().on_start(agent)
        self.survey_points = randint(2, 5)

    def perform(self, agent):
        # perform the action

        if distance(agent.position, self.target) <= 0:
            print("SPOT SAFE")
            self.points_visited += 1

        if self.points_visited >= self.survey_points:
            print("TERRITORY SAFE")
            self.finished = True
            agent.boredom = 0
            agent.social -= 50
        else:
            # next target
            self.target = self.__get_new_position()
            self.in_range = False

        return True

    def __get_new_position(self):
        pos = (randint(1, self.area), randint(1, self.area * 2))
        while pos in g_map.unpassable_tiles:
            pos = (randint(1, self.area), randint(1, self.area * 2))
        return Position(pos[0], pos[1])