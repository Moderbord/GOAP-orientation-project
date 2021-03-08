import custom_thread as c_thread
from game_server import g_map

from GOAP.transform import Position, distance

from GOAP2.working_memory import WorkingMemoryFact, FactType
from GOAP2.__sensor import __Sensor

class ResourceSensor(__Sensor):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 3
        self.scanning_location = Position(0, 0)
        self.scanning_radius = 5

    def _update(self):
        self.scanning_location = self.blackboard.get_position()
        self.perform_task()

    def scan_resources(self):
        # get scanning area
        (x_min, x_max) = max(0, self.scanning_location.x - self.scanning_radius), self.scanning_location.x + self.scanning_radius
        (y_min, y_max) = max(0, self.scanning_location.y - self.scanning_radius), self.scanning_location.y + self.scanning_radius
        # start scan
        for x in range(x_min, x_max):
            for y in range (y_min, y_max):
                tile = g_map.tile_data.get((x, y))
                if tile and tile.has_resources_remaining():
                    # create uniqe set of resources in tile
                    uniques = set()
                    for resource in tile.resource_list:
                        uniques.add(type(resource).__name__)

                    for resource in uniques:
                        fact = WorkingMemoryFact()
                        # confidence = distance to resource compared to max radius
                        resource_position = Position(x, y)
                        confidence = (float(self.scanning_radius) - float(distance(resource_position, self.scanning_location))) / float(self.scanning_radius) 
                        fact.set_pos(resource_position, confidence) # TODO use fact creation time as best memory instead?
                        fact.set_ftype(FactType.Resource)

                        if resource == "WildTree":
                            # TODO obj_confidence = blackboard get target object type == Logs ? 1.0 else 0.0
                            #fact.set_obj("Logs", obj_confidence)
                            fact.set_obj("Logs")
                        elif resource == "WildIronOre":
                            fact.set_obj("Ore")

                        # TODO always update fact (every confidence value must be updated)
                        if self.working_memory.query_fact(fact): # fact exists
                            _fact = self.working_memory.read_fact(fact) # retrieve it
                            _fact = fact # just update it
                            # if _fact.position.confidence < confidence: # if fact has less confidence than current -> update it
                            #     _fact.position.confidence = confidence
                            #     print("Updated fact")
                        else:
                            self.working_memory.create_fact(fact)
                            print("Created " + resource + " fact")

    def scan_result(self, result):
        pass

    def perform_task(self):
        #print("Scanning for resources..")
        thread = c_thread.BaseThread(
            target=self.scan_resources,
            target_args=(),
            callback=self.scan_result,
            callback_args=[]
        )
        thread.start()