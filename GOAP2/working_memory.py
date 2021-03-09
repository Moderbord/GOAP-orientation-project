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

    def __eq__(self, o: object) -> bool:
        tmp = []
        tmp.append(self.subject_id.value == o.subject_id.value)
        tmp.append(self.target_id.value == o.target_id.value)
        tmp.append(self.position.value == o.position.value)
        tmp.append(self.object.value == o.object.value)
        tmp.append(self.fact_type == o.fact_type)
        return all(tmp)
    
    def set_sid(self, value, cv=0.0):
        self.subject_id = _Attribute(value, cv)
        return self
    
    def set_tid(self, value, cv=0.0):
        self.target_id = _Attribute(value, cv)
        return self

    def set_pos(self, value, cv=0.0):
        self.position = _Attribute(value, cv)
        return self

    def set_obj(self, value, cv=0.0):
        self.object = _Attribute(value, cv)
        return self

    def set_ftype(self, value):
        self.fact_type = value
        return self

class WorkingMemory():

    def __init__(self) -> None:
        self.data = {}
        self.last_queried_fact = None

    def read_fact(self, fact):
        for f in self.data.get(fact.fact_type):
            if f == fact:
                return f
    
    def read_fact_where(self, function):
        return function(self.data)

    def read_fact_type_where(self, fact_type, function):
        return function(self.data.get(fact_type, []))

    def delete_fact_where(self, fact_type, function):
        facts = self.data.get(fact_type, [])
        for fact in facts:
            if function(fact):
                facts.remove(fact)

    def create_fact(self, fact):
        if self.data.get(fact.fact_type) is None:
            self.data[fact.fact_type] = [fact]
        else:
            self.data.get(fact.fact_type).append(fact)

    def query_fact(self, fact):
        return fact in self.data.get(fact.fact_type, [])

    def query_fact_type(self, fact_type) -> bool: # needed for implicit casting
        return self.data.get(fact_type)

    def get_fact_with_highest_confidence(self, fact_type, attribute):
        facts = self.data.get(fact_type, [])
        fact = max(facts, key=attribute, default=None)
        return fact

class WorkingMemoryManager():

    def __init__(self) -> None:
        self.agent_table = {}

    def create_working_memory(self, agent_id: int) -> WorkingMemory:
        working_memory = WorkingMemory()
        self.agent_table[agent_id] = working_memory
        return working_memory

    def get_working_memory(self, agent_id: int) -> WorkingMemory:
        return self.agent_table.get(agent_id)

g_wmm = WorkingMemoryManager()