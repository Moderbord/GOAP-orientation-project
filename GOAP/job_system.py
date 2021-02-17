from enum import Enum, auto
from queue import Queue

class JobType(Enum):
    Build = auto()
    Work = auto()
    Fetch = auto()
    Collect = auto()

class Job():

    def __init__(self, job_type, location, extra=None, callback=None) -> None:
        self.job_type = job_type
        self.location = location
        self.extra = extra
        self.callback = callback

class JobQueue():

    def __init__(self) -> None:
        self.__queue = Queue()

    def append(self, job):
        self.__queue.put(job)

    def get_job(self):
        return self.__queue.get()
    
    def has_job(self):
        return not self.__queue.empty()


