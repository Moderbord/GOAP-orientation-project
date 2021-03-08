import custom_thread as c_thread
from game_server import g_map

from GOAP.transform import Position, distance

from GOAP2.__sensor import __Sensor
from GOAP2.working_memory import WorkingMemoryFact, FactType, g_wmm
from GOAP2.blackboard import g_bbm

class ResourceSensor(__Sensor):

    def __init__(self) -> None:
        super().__init__()
        self.update_interval = 3
        self.scanning_location = Position(0, 0)
        self.scanning_radius = 5

    def _update(self, agent_id: int):
        self.scanning_location = g_bbm.get_blackboard(agent_id).get_position()
        self.perform_task(agent_id)

    def scan_resources(self, agent_id: int):
        # get scanning area
        (x_min, x_max) = max(0, self.scanning_location.x - self.scanning_radius), self.scanning_location.x + self.scanning_radius
        (y_min, y_max) = max(0, self.scanning_location.y - self.scanning_radius), self.scanning_location.y + self.scanning_radius
        #
        drop_loc = Position(2, 2) # TODO query value
        max_distance = distance(drop_loc, Position(g_map.tile_width, g_map.tile_height))
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
                        confidence = (float(max_distance) - float(distance(resource_position, drop_loc))) / float(max_distance) 
                        fact.set_pos(resource_position, confidence)
                        fact.set_ftype(FactType.Resource)

                        if resource == "WildTree":
                            # TODO? obj_confidence = blackboard get target object type == Logs ? 1.0 else 0.0
                            #fact.set_obj("Logs", obj_confidence)
                            fact.set_obj("Logs")
                        elif resource == "WildIronOre":
                            fact.set_obj("Ore")

                        # TODO always update fact (every confidence value must be updated)
                        if g_wmm.get_working_memory(agent_id).query_fact(fact): # fact exists
                            continue
                            # _fact = self.working_memory.read_fact(fact) # retrieve it
                            # _fact = fact # just update it
                            # if _fact.position.confidence < confidence: # if fact has less confidence than current -> update it
                            #     _fact.position.confidence = confidence
                            #     print("Updated fact")
                        else:
                            g_wmm.get_working_memory(agent_id).create_fact(fact)
                            #print("Created " + resource + " fact")

    def perform_task(self, agent_id: int):
        #print("Scanning for resources..")
        thread = c_thread.BaseThread(
            target=self.scan_resources,
            target_args=[agent_id]
        )
        thread.start()