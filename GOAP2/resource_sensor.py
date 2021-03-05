import custom_thread as c_thread
from game_server import g_map

from GOAP.transform import Position

from GOAP2.working_memory import WorkingMemoryFact, FactType
from GOAP2.__sensor import __Sensor

class ResourceSensor(__Sensor):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 3

    def _update(self):
        self.perform_task()

    def scan_resources(self):
        for x in range(4, 8):
            for y in range (1, 4):
                tile = g_map.tile_data.get((x, y))
                if tile and tile.has_resources_remaining():
                    fact = WorkingMemoryFact()
                    fact.set_pos(Position(x, y), float(x) / float(8)).set_ftype(FactType.Resource) # need to store type of resource
                    self.working_memory.create_fact(fact)
                    print("Created fact")

    def scan_result(self, result):
        pass

    def perform_task(self):
        print("Launching task..")
        thread = c_thread.BaseThread(
            target=self.scan_resources,
            target_args=(),
            callback=self.scan_result,
            callback_args=[]
        )
        thread.start()