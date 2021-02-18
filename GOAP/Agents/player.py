from collections import deque
from random import randint

import game_time as time

from GOAP.agent import GOAPAgent
from GOAP.providable import GOAPProvidable
from GOAP.transform import Position
from GOAP.action_set import ActionSet
from GOAP.job_system import Job, JobType
from GOAP.Agents.artisan import Profession

# Actions
from GOAP.Actions.Player.produce_worker import ProduceWorker
from GOAP.Actions.Player.assign_worker_logs import AssignWorkerLogs
from GOAP.Actions.Player.assign_worker_ore import AssignWorkerOre
from GOAP.Actions.Player.gather_resources import GatherResources

class Player(GOAPAgent, GOAPProvidable):

    def __init__(self, game_map, starting_location=Position()):
        super().__init__()
        self.data_provider = self
        self.resources = []
        self.units = []
        self.structures = []
        self.game_map = game_map
        self.starting_location = starting_location

        self.collect_jobs = deque()
        self.build_jobs = deque()
        self.upgrade_jobs = deque()
        self.fetch_jobs = []
        self.work_jobs = []

        self.ore_gatherers = 0
        self.logs_gatherers = 0

        # actions
        # self.add_action(ProduceWorker())
        # self.add_action(AssignWorkerLogs())
        # self.add_action(AssignWorkerOre())
        # self.add_action(GatherResources())

    def update(self):
        for unit in self.units:
            unit.update()
        for structure in self.structures:
            structure.update()
        super().update()

    def create_world_state(self):
        # Returns an evaluated set of the world state
        world_data = ActionSet()

        return world_data

    def create_goal_state(self):
        goal_state = ActionSet()
        goal_state.add("gatherResources", True)
        goal_state.add("haveFreeWorker", True)

        return goal_state

    def add_unit(self, unit):
        unit.owner = self
        unit.start_agent() # GOAP
        unit.groups = self.game_map.sprite_group_units
        unit.start_actor() # Draw
        self.units.append(unit)
    
    def remove_unit(self, unit):
        self.units.remove(unit)

    def add_structure(self, structure):
        structure.owner = self
        structure.start_agent() # GOAP
        structure.groups = self.game_map.sprite_group_structures
        structure.start_actor() # Draw
        self.structures.append(structure)

    def get_units(self, unit):
        return [x for x in self.units if type(x).__name__ == unit]

    def get_units_where(self, function):
        return [x for x in self.units if function(x)]

    def get_unit_type_where(self, unit, function):
        return [x for x in self.get_units(unit) if function(x)]

    def count_units(self, unit):
        return len([x for x in self.units if type(x).__name__ == unit])

    def count_unit_type_where(self, unit, function):
        return len([x for x in self.get_units(unit) if function(x)])

    def get_structure(self, target):
        structure = [x for x in self.structures if type(x).__name__ == target]
        return structure[0] if structure else None

    def get_structure_where(self, function):
        structure = [x for x in self.structures if function(x)]
        return structure[0] if structure else None

    def add_resource(self, resource):
        self.resources.append(resource)

    def has_resource(self, target_resource):
        for resources in self.resources:
            if resources == target_resource:
                return True
        return False

    def remove_resource(self, resource, amount=1):
        if self.resources.count(resource) >= amount:
            for i in amount:
                self.resources.remove(resource)
            return True
        
        print("Not enough resources to deduct!")
        return False

    def count_resource(self, resource):
        return len([x for x in self.resources if type(x).__name__ == resource])

    def get_resource_drop_off_loc(self):
        return Position(2, 4)
    
    def get_resource_location(self, resource):
        if resource == "Ore":
            return Position(randint(8, 10), randint(2, 4))
        elif resource == "Logs":
            return Position(randint(1, 4), randint(6, 9))

    def add_job(self, job):
        if job.job_type == JobType.Build:
            self.build_jobs.append(job)

            # maximum num of builders?
            camp = self.get_structure("Camp") 
            upgrade_job = Job(JobType.Upgrade, camp.position, Profession.Builder, camp.on_upgrade)
            self.upgrade_jobs.append(upgrade_job)

        elif job.job_type == JobType.Collect:
            self.collect_jobs.append(job)

        elif job.job_type == JobType.Upgrade:
            self.upgrade_jobs.append(job)

        elif job.job_type == JobType.Work:
            self.work_jobs.append(job)

            # create upgrade job to cover work demand (should match)
            # units are upgraded at camp
            camp = self.get_structure("Camp") 
            upgrade_job = Job(JobType.Upgrade, camp.position, job.extra, camp.on_upgrade)
            self.upgrade_jobs.append(upgrade_job)

        elif job.job_type == JobType.Fetch:
            self.fetch_jobs.append(job)

    def has_job(self, job_type, artisan=None):

        if job_type == JobType.Build:
            return len(self.build_jobs) > 0

        elif job_type == JobType.Collect:
            return len(self.collect_jobs) > 0

        elif job_type == JobType.Upgrade:
            return len(self.upgrade_jobs) > 0

        elif job_type == JobType.Work:
            return len([job for job in self.work_jobs if job.extra == artisan]) > 0

        elif job_type == JobType.Fetch:
            return len([job for job in self.fetch_jobs if self.has_resource(job.extra)]) > 0

    def get_job(self, job_type, artisan=None):
        job = None
        # early out
        if not self.has_job(job_type, artisan):
            return job

        if job_type == JobType.Build:
            job = self.build_jobs.popleft()

        elif job_type == JobType.Collect:
            job = self.collect_jobs.popleft()

        elif job_type == JobType.Upgrade:
            job = self.upgrade_jobs.popleft()

        elif job_type == JobType.Work:
            index = 0
            for i in range(0, len(self.work_jobs)):
                if self.work_jobs[i].extra == artisan:
                    index = i
                    break
            job = self.work_jobs.pop(i)
                
        elif job_type == JobType.Fetch:
            index = 0
            for i in range(0, len(self.fetch_jobs)):
                if self.has_resource(self.fetch_jobs[i].extra) > 0:
                    index = i
                    break
            job = self.fetch_jobs.pop(i)

        return job

    def plan_found(self, goal, actions):
        pass

    def actions_finished(self):
        pass


