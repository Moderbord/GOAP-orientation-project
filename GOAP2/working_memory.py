from enum import Enum, auto

import game_time as time

# template T type
class _Attribute():

    def __init__(self, type, confidence=0.0) -> None:
        self.value = type
        self.confidence = confidence

class FactType(Enum):
    Collect = auto()
    Produce = auto()
    Resource = auto()
    Material = auto()
    Delivery = auto()

class Object(Enum):
    pass
    # TODO use this instead of strings?

class WorkingMemoryFact():

    fact_count = 0

    def __init__(self) -> None:
        self.subject_id = _Attribute(0)
        self.target_id = _Attribute(0)
        self.position = _Attribute(None)
        self.object = _Attribute(None)
        
        self.update_time = time.now()
        self.fact_id = WorkingMemoryFact.fact_count
        self.fact_type = None
        
        WorkingMemoryFact.fact_count += 1
    
    def set_sid(self, value, cv):
        self.subject_id = _Attribute(value, cv)
        return self
    
    def set_tid(self, value, cv):
        self.target_id = _Attribute(value, cv)
        return self

    def set_pos(self, value, cv):
        self.position = _Attribute(value, cv)
        return self

    def set_obj(self, value, cv):
        self.object = _Attribute(value, cv)
        return self

    def set_ftype(self, value):
        self.fact_type = value
        return self

class WorkingMemory():

    def __init__(self) -> None:
        self.data = {}

    def read_fact(self):
        pass

    def create_fact(self, fact):
        if self.data.get(fact.fact_type) is None:
            self.data[fact.fact_type] = [fact]
        else:
            self.data.get(fact.fact_type).append(fact)

    def query_fact(self):
        pass

    def get_fact_with_highest_confidence(self, fact_type, attribute):
        facts = self.data.get(fact_type, [])
        fact = max(facts, key=attribute, default=None)
        return fact