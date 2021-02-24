from GOAP.Actions.Structures.produce_unit import ProduceUnit
from GOAP.transform import Position
from GOAP.job_system import JobType

from GOAP.Agents.soldier import Soldier

class ProduceSoldier(ProduceUnit):

    def __init__(self):
        super().__init__()
        # production specific
        #self.target_unit = "Soldier"
        self.precursor_unit = "Worker"
        self.message_on_finish = "finished producing soldier."
        #self.production_requirements = {"Sword" : 1}
        self.production_time = 5

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("hasMaterials", True)
        self.add_precondition("produceSoldier", True)
        
        # effects
        self.add_effect("doJob", True)

    def on_production_finish(self):
        new_unit = Soldier()
        new_unit.position = Position(self.agent_position.x, self.agent_position.y)
        self.add_player_unit(new_unit)