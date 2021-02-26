from enum import Enum, auto

import game_time as time

# template T type
class __Attribute():

    def __init__(self, type) -> None:
        self.value = type
        self.confidence = 0.0

class FactType(Enum):
    Collect = auto()
    Produce = auto()
    Resource = auto()

class WorkingMemoryFact():

    fact_count = 0

    def __init__(self) -> None:
        self.subject_id = __Attribute(0)
        self.target_id = __Attribute(0)
        self.position = __Attribute(None)
        self.object = __Attribute(None)
        
        self.update_time = time.now()
        self.fact_id = WorkingMemoryFact.fact_count
        self.fact_type = None
        
        WorkingMemoryFact.fact_count += 1

class WorkingMemory():

    def __init__(self) -> None:
        self.data = []

    def read_fact(self):
        pass

    def create_fact(self):
        pass

    def query_fact(self):
        pass

    def get_fact_with_highest_confidence(self):
        pass