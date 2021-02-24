from GOAP.transform import Position
from pygame import Surface

from game_settings import g_vars

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.game_actor import GameActor

class Structure(GOAPAgent, GameActor, GOAPProvidable):

    def __init__(self):
        GOAPAgent.__init__(self)
        self.data_provider = self
        self.tile_color = g_vars["Structure"]["Base"]["TileColor"]
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        GameActor.__init__(self)
        self.position = Position(0, 0)
        
        # local variables
        self.structure_name = "Base"
        self.construction_time = 0
        self.construction_materials = {}
        self.is_built = False
        self.is_worked = False
        self.has_materials = False
        self.production_ready = False

        # production
        self.inventory = []
        self.produce = []
        self.production_target = ""
        self.production_table = {}
        self.required_artisan = None

    def update(self):
        GOAPAgent.update(self)
        GameActor.update(self)

    def inventory_update(self):
        production_target_requirements = self.production_table.get(self.production_target, {}) if self.is_built else self.construction_materials
        self.has_materials = all([self.inventory.count(key) >= production_target_requirements.get(key) for key in production_target_requirements.keys()])

    def on_built(self):
        self.is_built = True
        self.inventory.clear()
        self.inventory_update()

        self.tile_color = g_vars["Structure"][self.structure_name]["TileColor"]
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        #print(self.structure_name + " built!")

    def on_worked(self):
        self.is_worked = True
        #print(self.structure_name + " operational!")
    
    def on_production_begin(self):
        self.production_ready = True
    
        for material, amount in self.production_table.get(self.production_target).items():
            for x in range(amount):
                self.inventory.remove(material)

    def on_fetched(self, resource):
        self.inventory.append(resource)
        self.inventory_update()        

    def on_collected(self):
        if len(self.produce) > 0:
            self.produce.pop()
            return True
        else:
            print("ERROR NO PRODUCE COLLECTED")
            return False
