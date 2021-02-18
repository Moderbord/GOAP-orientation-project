from enum import Enum, auto

class JobType(Enum):
    Build = auto()
    Work = auto()
    Fetch = auto()
    Collect = auto()
    Upgrade = auto()

class Job():

    def __init__(self, job_type, location, extra=None, callback=None) -> None:
        self.job_type = job_type
        self.location = location
        self.extra = extra
        self.callback = callback
