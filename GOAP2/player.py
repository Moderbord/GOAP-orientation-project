from collections import deque

from GOAP.transform import Position
from GOAP.job_system import Job2, JobType

class Player():

    def __init__(self) -> None:
        self.resources = []

        self.units = []
        self.structures = []

        self.build_jobs = deque()
        self.collect_jobs = deque()
        self.upgrade_jobs = []
        self.production_jobs = []
        self.fetch_jobs = []
        self.work_jobs = []

        # tmp
        self.have_builder = False

    def update(self):
        for unit in self.units:
            unit.update()
        for structure in self.structures:
            structure.update()

    def render(self, screen, camera):
        for structure in self.structures:
            structure.entity.render(screen, camera)
        for unit in self.units:
            unit.entity.render(screen, camera)

    def add_unit(self, unit):
        self.units.append(unit)
    
    def remove_unit(self, unit):
        self.units.remove(unit)

    def add_structure(self, structure):
        self.structures.append(structure)

    def add_resource(self, resource):
        self.resources.append(resource)

    def has_resource(self, target_resource):
        return target_resource in self.resources

    def remove_resource(self, resource, amount=1):
        if self.resources.count(resource) >= amount:
            for i in range(0, amount):
                self.resources.remove(resource)
            return True
        
        print("Not enough resources to deduct!")
        return False

    def count_resource(self, resource):
        return len([x for x in self.resources if x == resource])

    def get_resource_drop_off_loc(self):
        return Position(2, 4)
    
    # def get_resource_location(self, resource):
    #     if resource == "Ore":
    #         return Position(randint(8, 10), randint(2, 4))
    #     elif resource == "Logs":
    #         return Position(randint(1, 4), randint(6, 9))

    def add_job(self, job):
        if job.job_type == JobType.Production:
            self.production_jobs.append(job)

        elif job.job_type == JobType.Build:
            self.build_jobs.append(job)

            # maximum num of builders?
            if not self.have_builder:
                production_job = Job2(JobType.Production, None, None, "Artisan")
                self.production_jobs.append(production_job)
                self.have_builder = True

                # for x in range(20):
                #     production_job = Job(JobType.Production, None, "Soldier") # tmp
                #     self.production_jobs.append(production_job)

        elif job.job_type == JobType.Collect:
            self.collect_jobs.append(job)

        elif job.job_type == JobType.Upgrade:
            self.upgrade_jobs.append(job)

        elif job.job_type == JobType.Work:
            self.work_jobs.append(job)

            # create unit to cover job
            production_job = Job2(JobType.Production, None, None, "Artisan")
            self.production_jobs.append(production_job)

        elif job.job_type == JobType.Fetch:
            self.fetch_jobs.append(job)

    def has_job(self, job_type, criteria=None):

        if job_type == JobType.Build:
            return len(self.build_jobs) > 0

        elif job_type == JobType.Collect:
            return len(self.collect_jobs) > 0

        elif job_type == JobType.Upgrade:
            return len([job for job in self.upgrade_jobs if job.extra == criteria]) > 0 # unit must match precursor

        elif job_type == JobType.Production:
            return len([job for job in self.production_jobs if job.extra in criteria]) > 0 # must be able to produce any production target 

        elif job_type == JobType.Work:
            return len([job for job in self.work_jobs if job.extra == criteria]) > 0 # artisan profession must match any jobs requirement

        elif job_type == JobType.Fetch:
            return len([job for job in self.fetch_jobs if self.has_resource(job.extra)]) > 0 # one resource of target type must exist in resource pile

    def get_job(self, job_type, criteria=None) -> Job2:
        job = None
        # early out
        if not self.has_job(job_type, criteria):
            return job

        if job_type == JobType.Build:
            job = self.build_jobs.popleft()

        elif job_type == JobType.Collect:
            job = self.collect_jobs.popleft()

        elif job_type == JobType.Upgrade:
            job = self.__job_finder(self.upgrade_jobs, lambda x: x == criteria)

        elif job_type == JobType.Production:
            job = self.__job_finder(self.production_jobs, lambda x: x in criteria)

        elif job_type == JobType.Work:
            job = self.__job_finder(self.work_jobs, lambda x: x == criteria)
                
        elif job_type == JobType.Fetch:
            job = self.__job_finder(self.fetch_jobs, lambda x: self.has_resource(x) > 0)

        return job
    
    def __job_finder(self, job_list, condition):
        index = 0
        for i in range(0, len(job_list)):
            if condition(job_list[i].extra):
                index = i
                break
        return job_list.pop(i)

g_player = Player()