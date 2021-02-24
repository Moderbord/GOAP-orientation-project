from GOAP.Actions.Structures.produce_unit import ProduceUnit
from GOAP.transform import Position
from GOAP.job_system import JobType

from GOAP.Agents.artisan import Artisan

class ProduceArtisan(ProduceUnit):

    def __init__(self):
        super().__init__()
        # production specific
        #self.target_unit = "Artisan"
        self.precursor_unit = "Worker"
        self.message_on_finish = "finished producing artisan."
        #self.production_requirements = {}
        self.production_time = 5

        # preconditions
        self.add_precondition("isBuilt", True)
        self.add_precondition("produceArtisan", True)
        
        # effects
        self.add_effect("doJob", True)
        
    def on_production_finish(self):
        new_unit = Artisan()
        new_unit.position = Position(self.agent_position.x, self.agent_position.y)
        self.add_player_unit(new_unit)