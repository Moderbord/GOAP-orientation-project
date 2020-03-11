from pygame import sprite
from pygame import Surface
from random import randint
from enum import Enum, auto

import entity_state as states
import state_machine as fsm
import message_dispatcher as dispatcher
import game_time as time
from game_settings import g_vars

#----------------------------BASE--------------------------------------#
class BasicGameEntity(sprite.Sprite):

    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        sprite.Sprite.__init__(self, self.groups)
        self.owner = owner
        self.fsm = fsm.StateMachine(self)
        self.fsm.currentState = states.State() # empty state
        # reference to map
        self.gamemap = owner.gamemap
        self.production_time = 0
        self.location = owner.start_position
        self.is_visible = False
        self.is_idle = False

    def begin_production(self):
        pass

    def spawn(self):
        #sprite/asset
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()
        # initial draw
        self.is_visible = True
        self.rect.x = self.location[0] * g_vars["Game"]["TileSize"] + g_vars["Game"]["TileSize"] / 3
        self.rect.y = self.location[1] * g_vars["Game"]["TileSize"] + g_vars["Game"]["TileSize"] / 3
        # state
        self.fsm.change_state(states.StateIdle())

    def update(self):
        # drawing
        if self.is_visible:
            self.rect.x = self.location[0] * g_vars["Game"]["TileSize"] + g_vars["Game"]["TileSize"] / 3
            self.rect.y = self.location[1] * g_vars["Game"]["TileSize"] + g_vars["Game"]["TileSize"] / 3
        # state machine
        self.fsm.update()

    def delete(self):
        sprite.Sprite.remove(self, self.groups)

#----------------------------UNITS--------------------------------------#
class BasicGameUnit(BasicGameEntity):

    def __init__(self, owner):
        self.image = Surface((g_vars["Game"]["UnitSize"], g_vars["Game"]["UnitSize"]))
        BasicGameEntity.__init__(self, owner)
        self.move_factor = g_vars["Unit"]["Basic"]["MoveFactor"]
        self.move_progress = 0

        # pathfinding
        self.is_finding_path = False
        self.is_traversing = False
        self.current_path = None
        self.current_tile = None
        self.next_tile = None

    def set_path(self, path):
        self.current_path = path
        self.current_tile = self.gamemap.get_background_tile(self.location)
        self.next_tile = path[self.location]

    def stop_pathing(self):
        self.current_path = None
        self.next_tile = None

    def move(self, dx=0, dy=0):
        new_pos = self.location[0] + dx, self.location[1] + dy
        self.location = new_pos
        self.current_tile = self.gamemap.get_background_tile(new_pos)

    def update(self):
        # movement
        if self.current_path:

            if self.next_tile is None:
                self.current_path = None
                # message telling the entity that is has arrived
                message = dispatcher.Message(self, dispatcher.MSG.ArrivedAtGoal)
                self.fsm.handle_message(message)
            
            else:
                (x1, y1) = self.location
                (x2, y2) = self.next_tile
                dx, dy = x2 - x1, y2 - y1
                # get required movement threshold
                threshold = self.current_tile.movement_straight if (dx * dy == 0) else self.current_tile.movement_diagonal
                # take movement factor into account
                self.move_progress += time.delta_time * self.move_factor
                if self.move_progress >= threshold:
                    # reset progress
                    self.move_progress = 0
                    # move
                    self.move(dx, dy)
                    # update next tile
                    self.next_tile = self.current_path[self.next_tile]
            
        super().update()

class UnitWorker(BasicGameUnit):
    def __init__(self, owner):
        self.tile_color = g_vars["Unit"]["Worker"]["TileColor"]
        BasicGameUnit.__init__(self, owner)
        self.move_factor = g_vars["Unit"]["Worker"]["MoveFactor"]
        self.production_time = g_vars["Unit"]["Worker"]["ProductionTime"]
        self.carried_resource = None

    def begin_production(self):
        # get structure
        self.origin_structure = self.owner.get_available_structure(StructureCamp)
        #print("Got free Camp")
        # occupy structure
        self.origin_structure.fsm.change_state(states.StateLocked())
        #print("Locked Camp")
        # change to production state
        self.fsm.change_state(states.StateProduced())

    def production_spawn(self):
        # position to building
        self.location = self.origin_structure.location
        # spawn
        super().spawn()
        # notify owner
        message = dispatcher.Message(self, dispatcher.MSG.NewWorkerUnit)
        self.owner.fsm.handle_message(message)
        # free structure
        self.origin_structure.fsm.change_state(states.StateIdle())

class UnitExplorer(BasicGameUnit):
    def __init__(self, owner):
        self.tile_color = g_vars["Unit"]["Explorer"]["TileColor"]
        BasicGameUnit.__init__(self, owner)
        self.move_factor = g_vars["Unit"]["Explorer"]["MoveFactor"]
        self.production_time = g_vars["Unit"]["Explorer"]["ProductionTime"]

    def begin_production(self):
        # find free worker
        self.worker_unit = self.owner.get_available_unit(UnitWorker)
        # pause worker for production time
        self.worker_unit.fsm.change_state(states.StateLocked())
        # change to production state
        self.fsm.change_state(states.StateProduced())

    def production_spawn(self):
        # put explorer where worker stood
        self.location = self.worker_unit.location
        super().spawn()
        # clear any fog
        self.gamemap.discover_fog_area((self.location[0] - 1, self.location[1] - 1), (self.location[0] + 1, self.location[1] + 1))
        # remove worker
        self.owner.remove_unit(self.worker_unit)
        # notify owner
        message = dispatcher.Message(self, dispatcher.MSG.NewExplorerUnit)
        self.owner.fsm.handle_message(message)

    def move(self, dx=0, dy=0):
        new_pos = self.location[0] + dx, self.location[1] + dy
        self.location = new_pos                               

        new_resources = {}

        if dx: # horizontal movement
            start = (new_pos[0] + dx, new_pos[1] - 1)
            stop = (new_pos[0] + dx, new_pos[1] + 1)
            new_resources.update(self.gamemap.discover_fog_area(start, stop))
        if dy: # vertical movement
            start = (new_pos[0] - 1, new_pos[1] + dy)
            stop = (new_pos[0] + 1, new_pos[1] + dy)
            new_resources.update(self.gamemap.discover_fog_area(start, stop))
            
        if new_resources:
            self.owner.resource_map.update(new_resources)


class UnitArtisan(BasicGameUnit):

    class Profession(Enum):
        Free = auto()
        Refiner = auto()
        Smith = auto()
        Builder = auto()
        Smelter = auto()

    def __init__(self, owner):
        self.tile_color = g_vars["Unit"]["Artisan"]["TileColor"]
        BasicGameUnit.__init__(self, owner)
        self.move_factor = g_vars["Unit"]["Artisan"]["MoveFactor"]
        self.production_time = g_vars["Unit"]["Artisan"]["ProductionTime"]
        self.profession = self.Profession.Free

    def begin_production(self):
        # find free worker
        self.worker_unit = self.owner.get_available_unit(UnitWorker)
        # pause worker for production time
        self.worker_unit.fsm.change_state(states.StateLocked())
        # change to production state
        self.fsm.change_state(states.StateProduced())

    def production_spawn(self):
        # put explorer where worker stood
        self.location = self.worker_unit.location
        super().spawn()
        # remove worker
        self.owner.remove_unit(self.worker_unit)
        # notify owner
        message = dispatcher.Message(self, dispatcher.MSG.NewArtisanUnit)
        self.owner.fsm.handle_message(message)

class UnitSoldier(BasicGameUnit):
    def __init__(self, owner):
        self.tile_color = g_vars["Unit"]["Soldier"]["TileColor"]
        BasicGameUnit.__init__(self, owner)
        self.move_factor = g_vars["Unit"]["Soldier"]["MoveFactor"]
        self.production_time = g_vars["Unit"]["Soldier"]["ProductionTime"]

    def begin_production(self):
        # find free worker
        self.worker_unit = self.owner.get_available_unit(UnitWorker)
        # pause worker for production time
        self.worker_unit.fsm.change_state(states.StateLocked()) # change to become soldier
        # change to production state
        self.fsm.change_state(states.StateProduced())

    def production_spawn(self):
        # put explorer where worker stood
        self.location = self.worker_unit.location
        super().spawn()
        # remove worker
        self.owner.remove_unit(self.worker_unit)
        # notify owner
        message = dispatcher.Message(self, dispatcher.MSG.NewSoldierUnit)
        self.owner.fsm.handle_message(message)

#----------------------------STRUCTURES--------------------------------------#
class BasicGameStructure(BasicGameEntity):
    def __init__(self, owner):
        self.image = Surface((g_vars["Game"]["StructureSize"], g_vars["Game"]["StructureSize"]))
        BasicGameEntity.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Base"]["ProductionTime"]
        self.output = g_vars["Structure"]["Base"]["Output"]
        self.artisan_unit = None
        self.artisan_required = None
    
    def begin_production(self):
        # find free building tile
        tile = self.owner.get_buildable_tile()
        # occupy it
        self.owner.gamemap.occupy_tile(tile)
        # spawn structure base
        self.structure_base = StructureBase(self.owner)
        self.structure_base.location = tile.location
        self.structure_base.spawn()
        self.owner.add_structure(self.structure_base)
        # set position to base (for artisan unit)
        self.location = self.structure_base.location
        # specify required artisan
        self.artisan_required = UnitArtisan.Profession.Builder
        # change to wait for builder state
        self.fsm.change_state(states.StateWaitForArtisan())

    def production_spawn(self):
        super().spawn()
        # remove base
        self.owner.remove_structure(self.structure_base)
        # release builder
        self.artisan_unit.fsm.change_state(states.StateArtisan())

class StructureBase(BasicGameStructure):
    def __init__(self, owner):
        self.tile_color = g_vars["Structure"]["Base"]["TileColor"]
        BasicGameStructure.__init__(self, owner)

class StructureCamp(BasicGameStructure):
    def __init__(self, owner):
        self.tile_color = g_vars["Structure"]["Camp"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Camp"]["ProductionTime"]
        self.output = g_vars["Structure"]["Camp"]["Output"]

class StructureSmithy(BasicGameStructure):
    def __init__(self, owner):
        self.tile_color = g_vars["Structure"]["Smithy"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Smithy"]["ProductionTime"]
        self.output = g_vars["Structure"]["Smithy"]["Output"]
    
    def production_spawn(self):
        super().production_spawn()
        # specify required artisan
        self.artisan_required = UnitArtisan.Profession.Smith
        # change to wait for builder state
        self.fsm.change_state(states.StateWaitForArtisan())
    
class StructureSmelter(BasicGameStructure):
    def __init__(self, owner):
        self.tile_color = g_vars["Structure"]["Smelter"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Smelter"]["ProductionTime"]
        self.output = g_vars["Structure"]["Smelter"]["Output"]

    def production_spawn(self):
        super().production_spawn()
        # specify required artisan
        self.artisan_required = UnitArtisan.Profession.Smelter
        # change to wait for builder state
        self.fsm.change_state(states.StateWaitForArtisan())

class StructureRefinery(BasicGameStructure):
    def __init__(self, owner):
        self.tile_color = g_vars["Structure"]["Refinery"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Refinery"]["ProductionTime"]
        self.output = g_vars["Structure"]["Refinery"]["Output"]

    def production_spawn(self):
        super().production_spawn()
        # specify required artisan
        self.artisan_required = UnitArtisan.Profession.Refiner
        # change to wait for builder state
        self.fsm.change_state(states.StateWaitForArtisan())
    
class StructureEncampment(BasicGameStructure):
    def __init__(self, owner):
        self.tile_color = g_vars["Structure"]["Encampment"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Encampment"]["ProductionTime"]
        self.output = g_vars["Structure"]["Encampment"]["Output"]

#----------------------------RESOURCES??--------------------------------------#
class BasicMapResource(sprite.Sprite):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_resources
        sprite.Sprite.__init__(self, self.groups)
        self.image = Surface((g_vars["Game"]["ResourceSize"], g_vars["Game"]["ResourceSize"]))
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * g_vars["Game"]["TileSize"] + randint(0, g_vars["Game"]["TileSize"])
        self.rect.y = location[1] * g_vars["Game"]["TileSize"] + randint(0, g_vars["Game"]["TileSize"])

class WildTree(BasicMapResource):
    def __init__(self, gamemap, location):
        self.tile_color = "Yellow"
        super().__init__(gamemap, location)
        self.gathered_type = g_vars["Exploration"]["WildTree"]["GatheredType"]

class WildIronOre(BasicMapResource):
    def __init__(self, gamemap, location):
        self.tile_color = "Gray"
        super().__init__(gamemap, location)
        self.gathered_type = g_vars["Exploration"]["WildIronOre"]["GatheredType"]    

class BasicResource(BasicMapResource):
    def __init__(self, owner):
        self.owner = owner
        self.tile_color = "Black"
        super().__init__(owner.gamemap, owner.start_position)
        self.fsm = fsm.StateMachine(self)
        self.fsm.currentState = states.State()
        self.origin_structure = None
        self.gathered_type = None

    def update(self):
        self.fsm.update()

    def production_spawn(self):
        # change state
        self.fsm.change_state(states.StateIdle())
        # free structure
        self.origin_structure.fsm.change_state(states.StateIdle())

class Tree(BasicResource):
    def __init__(self, owner):
        super().__init__(owner)

class IronOre(BasicResource):
    def __init__(self, owner):
        super().__init__(owner)
        self.gathered_type = g_vars["Exploration"]["IronOre"]["GatheredType"]

class Coal(BasicResource):
    def __init__(self, owner):
        super().__init__(owner)
        self.production_time = g_vars["Resource"]["Coal"]["ProductionTime"]

    def begin_production(self):
        # get structure
        self.origin_structure = self.owner.get_available_structure(StructureRefinery)
        # occupy structure
        self.origin_structure.fsm.change_state(states.StateLocked())
        # change to production state
        self.fsm.change_state(states.StateProduced())

    def production_spawn(self):
        super().production_spawn()
        self.owner.add_resource(["Resource", "Coal", 1])

class IronBar(BasicResource):
    def __init__(self, owner):
        super().__init__(owner)
        self.production_time = g_vars["Resource"]["IronBar"]["ProductionTime"]

    def begin_production(self):
        # get structure
        self.origin_structure = self.owner.get_available_structure(StructureSmelter)
        # occupy structure
        self.origin_structure.fsm.change_state(states.StateLocked())
        # change to production state
        self.fsm.change_state(states.StateProduced())

    def production_spawn(self):
        super().production_spawn()
        self.owner.add_resource(["Resource", "IronBar", 1])

class Sword(BasicResource):
    def __init__(self, owner):
        super().__init__(owner)
        self.production_time = g_vars["Resource"]["Sword"]["ProductionTime"]

    def begin_production(self):
        # get structure
        self.origin_structure = self.owner.get_available_structure(StructureSmithy)
        # occupy structure
        self.origin_structure.fsm.change_state(states.StateLocked())
        # change to production state
        self.fsm.change_state(states.StateProduced())
        
    def production_spawn(self):
        super().production_spawn()
        self.owner.add_resource(["Resource", "Sword", 1])

#----------------------------JSON to python class----------------------------------#
def to_class(entity_type):
    #-----------UNITS-----------#
    if entity_type == "Worker":
        return UnitWorker
    if entity_type == "Explorer":
        return UnitExplorer
    if entity_type == "Artisan":
        return UnitArtisan
    if entity_type == "Soldier":
        return UnitSoldier
    #---------STRUCTURES--------#
    if entity_type == "Camp":
        return StructureCamp
    if entity_type == "Refinery":
        return StructureRefinery
    if entity_type == "Smelter":
        return StructureSmelter
    if entity_type == "Smithy":
        return StructureSmithy
    if entity_type == "Encampment":
        return StructureEncampment
    #----------RESOURCES--------#
    if entity_type == "WildTree":
        return WildTree
    if entity_type == "Tree":
        return Tree
    if entity_type == "Coal":
        return Coal
    if entity_type == "WildIronOre":
        return WildIronOre
    if entity_type == "IronOre":
        return IronOre
    if entity_type == "IronBar":
        return IronBar
    if entity_type == "Sword":
        return Sword