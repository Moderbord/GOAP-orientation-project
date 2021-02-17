import game_time as time

from GOAP.action import GOAPAction

class ProduceCoal(GOAPAction):

    def __init__(self):
        super().__init__()
        # local variables
        self.finished = False
        self.is_producing = False
        self.target_resource = "Coal"
        self.message_on_finish = "finished producing coal."
        self.progress = 0
        self.production_time = 4

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("isWorked", True)
        self.add_precondition("hasMaterials", True)
        
        # effects
        self.add_effect("hasProduce", True)

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
        if self.is_producing:
            self.progress += time.clock.delta

            if self.progress >= self.production_time:
                print(type(agent).__name__ + " " + self.message_on_finish)
                self.finished = True
                agent.produce.append(self.target_resource)

            return True

        if agent.has_materials:
            for material, amount in agent.required_materials.items():
                for x in range(amount):
                    agent.raw_materials.remove(material)
            
            self.is_producing = True

        return True