from pygame import sprite
from pygame import Surface

import entity_state as states
import state_machine as fsm
import message_dispatcher as dispatcher
from game_settings import g_vars

#----------------------------BASE--------------------------------------#
class BasicGameEntity(sprite.Sprite):

    def __init__(self, owner):
        sprite.Sprite.__init__(self, self.groups)
        self.owner = owner
        self.fsm = fsm.StateMachine(self)
        self.fsm.currentState = states.StateIdle()
        # reference to map
        self.gamemap = owner.gamemap
        self.production_time = 0
        self.location = owner.start_position
        self.is_idle = True

        #sprite/asset
        self.image = Surface((g_vars["Game"]["TileSize"], g_vars["Game"]["TileSize"]))
        self.image.fill(g_vars["Game"]["Colors"][self.tile_color])
        self.rect = self.image.get_rect()

    def update(self):
        # state machine
        self.fsm.Update()

#----------------------------UNITS--------------------------------------#
class BasicGameUnit(BasicGameEntity):

    def __init__(self, owner):
        BasicGameEntity.__init__(self, owner)
        self.move_speed = g_vars["Unit"]["Basic"]["MoveSpeed"]
        self.move_progress = 0

        # pathfinding
        self.is_finding_path = False
        self.is_traversing = False
        self.current_path = None
        self.next_tile = None

    def set_path(self, path):
        self.current_path = path
        self.next_tile = path[self.location]

    def stop_pathing(self):
        self.current_path = None
        self.next_tile = None

    def move(self, dx=0, dy=0):
        new_pos = self.location[0] + dx, self.location[1] + dy
        self.location = new_pos

    def update(self):
        super().update()

        # movement
        if self.current_path:
            (x1, y1), (x2, y2) = self.location, self.next_tile
            dx, dy = x2 - x1, y2 - y1
            # get current tile
            current_tile = self.gamemap.get_background_tile(self.location)
            # take movement factor into account
            self.move_progress += self.move_speed * current_tile.movement_factor
            if self.move_progress >= 100:
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
                self.fsm.HandleMessage(message)

        # drawing
        self.rect.x = self.location[0] * g_vars["Game"]["TileSize"]
        self.rect.y = self.location[1] * g_vars["Game"]["TileSize"]

class UnitWorker(BasicGameUnit):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Unit"]["Worker"]["TileColor"]
        BasicGameUnit.__init__(self, owner)
        self.move_speed = g_vars["Unit"]["Worker"]["MoveSpeed"]
        
        # notify owner
        message = dispatcher.Message(self, dispatcher.MSG.NewWorkerUnit)
        owner.fsm.HandleMessage(message)

class UnitExplorer(BasicGameUnit):
    def __init__(self, owner):
        self.groups = owner.gamemap.sprite_group_entities
        self.tile_color = g_vars["Unit"]["Explorer"]["TileColor"]
        BasicGameUnit.__init__(self, owner)
        self.move_speed = g_vars["Unit"]["Explorer"]["MoveSpeed"]
        self.production_time = g_vars["Unit"]["Explorer"]["ProductionTime"]
        
        # notify owner
        message = dispatcher.Message(self, dispatcher.MSG.NewExplorerUnit)
        owner.fsm.HandleMessage(message)

    def move(self, dx=0, dy=0):
        new_pos = self.location[0] + dx, self.location[1] + dy
        self.location = new_pos                               
        
        if dx: # horizontal movement
            start = (new_pos[0] + dx, new_pos[1] - 1)
            stop = (new_pos[0] + dx, new_pos[1] + 1)
            self.gamemap.clear_fog_area(start, stop)
        if dy: # vertical movement
            start = (new_pos[0] - 1, new_pos[1] + dy)
            stop = (new_pos[0] + 1, new_pos[1] + dy)
            self.gamemap.clear_fog_area(start, stop)

class UnitArtisan(BasicGameUnit):
    #profession
    pass

class UnitSoldier(BasicGameUnit):
    pass

#----------------------------STRUCTURES--------------------------------------#
class BasicGameStructure(BasicGameEntity):
    def __init__(self, owner):
        BasicGameEntity.__init__(self, owner)
        self.output = {}

    def update(self):
        super().update()

class StructureSmithy(BasicGameStructure):
    #swords
    pass

class StructureSmelter(BasicGameStructure):
    #iron bars
    pass

class StructureRefinery(BasicGameStructure):
    #coal
    pass

class StructureEncampment(BasicGameStructure):
    #soldiers
    pass


#----------------------------RESOURCES??--------------------------------------#
class BasicResource(BasicGameEntity):
    def __init__(self, owner):
        BasicGameEntity.__init__(self, owner)

class Tree(BasicResource):
    pass

class Coal(BasicResource):
    pass

class IronOre(BasicResource):
    pass

class IronBar(BasicResource):
    pass

class Sword(BasicResource):
    pass


#----------------------------JSON to python class----------------------------------#
def To_Class(entity_type):
    if entity_type == "Worker":
        return UnitWorker
    if entity_type == "Explorer":
        return UnitExplorer