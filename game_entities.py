from pygame import sprite
from pygame import Surface
from random import randint

import entity_state as states
import state_machine as fsm
import message_dispatcher as dispatcher
import game_time as time
from game_settings import g_vars

#----------------------------BASE--------------------------------------#
class BasicGameEntity(sprite.Sprite):

    def __init__(self, owner):
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
        self.image = Surface((g_vars["Game"]["TileSize"], g_vars["Game"]["TileSize"]))
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()
        # dirty fix
        self.is_visible = True
        self.rect.x = self.location[0] * g_vars["Game"]["TileSize"]
        self.rect.y = self.location[1] * g_vars["Game"]["TileSize"]

    def update(self):
        # drawing
        if self.is_visible:
            self.rect.x = self.location[0] * g_vars["Game"]["TileSize"]
            self.rect.y = self.location[1] * g_vars["Game"]["TileSize"]
        # state machine
        self.fsm.update()

    def delete(self):
        sprite.Sprite.remove(self, self.groups)

#----------------------------UNITS--------------------------------------#
class BasicGameUnit(BasicGameEntity):

    def __init__(self, owner):
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
            (x1, y1), (x2, y2) = self.location, self.next_tile
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
            
            if self.next_tile is None:
                self.current_path = None
                # message telling the entity that is has arrived
                message = dispatcher.Message(self, dispatcher.MSG.ArrivedAtGoal)
                self.fsm.handle_message(message)

        super().update()


class UnitWorker(BasicGameUnit):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
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

    def spawn(self):
        # position to building
        self.location = self.origin_structure.location
        # spawn
        super().spawn()
        #print("Spawning")
        # change state
        self.fsm.change_state(states.StateIdle())
        # notify owner
        message = dispatcher.Message(self, dispatcher.MSG.NewWorkerUnit)
        self.owner.fsm.handle_message(message)
        # free structure
        self.origin_structure.fsm.change_state(states.StateIdle())
        #print("Released Camp")

class UnitExplorer(BasicGameUnit):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Unit"]["Explorer"]["TileColor"]
        BasicGameUnit.__init__(self, owner)
        self.move_factor = g_vars["Unit"]["Explorer"]["MoveFactor"]
        self.production_time = g_vars["Unit"]["Explorer"]["ProductionTime"]

    def begin_production(self):
        # find free worker
        self.worker_unit = self.owner.get_available_unit(UnitWorker)
        #print("Got free Worker")
        # pause worker for production time
        self.worker_unit.fsm.change_state(states.StateLocked())
        #print("Locked Worker")
        # change to production state
        self.fsm.change_state(states.StateProduced())

    def spawn(self):
        # put explorer where worker stood
        self.location = self.worker_unit.location
        super().spawn()
        #print("Re-Spawning")
        self.fsm.change_state(states.StateIdle())
        # clear any fog
        self.gamemap.discover_fog_area((self.location[0] - 1, self.location[1] - 1), (self.location[0] + 1, self.location[1] + 1))
        # remove worker
        self.owner.remove_unit(self.worker_unit)
        #print("Removed Worker")
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
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Unit"]["Artisan"]["TileColor"]
        BasicGameUnit.__init__(self, owner)
        self.move_factor = g_vars["Unit"]["Artisan"]["MoveFactor"]
        self.production_time = g_vars["Unit"]["Artisan"]["ProductionTime"]

    def begin_production(self):
        # find free worker
        self.worker_unit = self.owner.get_available_unit(UnitWorker)
        # pause worker for production time
        self.worker_unit.fsm.change_state(states.StateLocked())
        # change to production state
        self.fsm.change_state(states.StateProduced())

    def spawn(self):
        # put explorer where worker stood
        self.location = self.worker_unit.location
        super().spawn()
        self.fsm.change_state(states.StateIdle())
        # remove worker
        self.owner.remove_unit(self.worker_unit)
        # notify owner
        message = dispatcher.Message(self, dispatcher.MSG.NewArtisanUnit)
        self.owner.fsm.handle_message(message)

class UnitSoldier(BasicGameUnit):
    pass

#----------------------------STRUCTURES--------------------------------------#
class BasicGameStructure(BasicGameEntity):
    def __init__(self, owner):
        BasicGameEntity.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Base"]["ProductionTime"]
        self.output = g_vars["Structure"]["Base"]["Output"]
    
    def begin_production(self):
        # find free building tile
        tile = self.owner.get_buildable_tile()
        #print("Got free building tile")
        # spawn structure base
        self.structure_base = StructureBase(self.owner)
        self.structure_base.location = tile.location
        self.structure_base.spawn()
        #print("Structure base placed")
        # change to production state
        self.fsm.change_state(states.StateProduced())

class StructureBase(BasicGameStructure):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Structure"]["Base"]["TileColor"]
        BasicGameStructure.__init__(self, owner)

class StructureCamp(BasicGameStructure):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Structure"]["Camp"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Camp"]["ProductionTime"]
        self.output = g_vars["Structure"]["Camp"]["Output"]

    def spawn(self):
        # set position to base
        self.location = self.structure_base.location
        super().spawn()
        # state
        self.fsm.change_state(states.StateIdle())
        # remove base
        self.structure_base.delete()

class StructureSmithy(BasicGameStructure):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Structure"]["Smithy"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Smithy"]["ProductionTime"]
        self.output = g_vars["Structure"]["Smithy"]["Output"]
    
    def spawn(self):
        # set position to base
        self.location = self.structure_base.location
        super().spawn()
        # state
        self.fsm.change_state(states.StateIdle())
        # remove base
        self.structure_base.delete()

class StructureSmelter(BasicGameStructure):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Structure"]["Smelter"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Smelter"]["ProductionTime"]
        self.output = g_vars["Structure"]["Smelter"]["Output"]

        def spawn(self):
            # set position to base
            self.location = self.structure_base.location
            super().spawn()
            # state
            self.fsm.change_state(states.StateIdle())
            # remove base
            self.structure_base.delete()

class StructureRefinery(BasicGameStructure):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Structure"]["Refinery"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Refinery"]["ProductionTime"]
        self.output = g_vars["Structure"]["Refinery"]["Output"]
    
    def spawn(self):
        # set position to base
        self.location = self.structure_base.location
        super().spawn()
        # state
        self.fsm.change_state(states.StateIdle())
        # remove base
        self.structure_base.delete()
        
class StructureEncampment(BasicGameStructure):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Structure"]["Encampment"]["TileColor"]
        BasicGameStructure.__init__(self, owner)
        self.production_time = g_vars["Structure"]["Encampment"]["ProductionTime"]
        self.output = g_vars["Structure"]["Encampment"]["Output"]
    
    def spawn(self):
        # set position to base
        self.location = self.structure_base.location
        super().spawn()
        # state
        self.fsm.change_state(states.StateIdle())
        # remove base
        self.structure_base.delete()

#----------------------------RESOURCES??--------------------------------------#
class BasicResource(sprite.Sprite):
    def __init__(self, location):
        sprite.Sprite.__init__(self, self.groups)
        self.image = Surface((g_vars["Game"]["ResourceSize"], g_vars["Game"]["ResourceSize"]))
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * g_vars["Game"]["TileSize"] + randint(0, g_vars["Game"]["TileSize"])
        self.rect.y = location[1] * g_vars["Game"]["TileSize"] + randint(0, g_vars["Game"]["TileSize"])
        self.gathered_type = None 

class WildTree(BasicResource):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_resources
        self.tile_color = "Yellow"
        super().__init__(location)
        self.gathered_type = g_vars["Exploration"]["WildTree"]["GatheredType"]

class Tree(BasicResource):
    pass

class Coal(BasicResource):
    pass

class IronOre(BasicResource):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_resources
        self.tile_color = "Yellow"
        super().__init__(location)
        self.gathered_type = g_vars["Exploration"]["IronOre"]["GatheredType"]

class IronBar(BasicResource):
    pass

class Sword(BasicResource):
    pass


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
    if entity_type == "IronOre":
        return IronOre
    if entity_type == "IronBar":
        return IronBar
    if entity_type == "Sword":
        return Sword