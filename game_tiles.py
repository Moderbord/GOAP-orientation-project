from pygame import sprite
from pygame import Surface

import game_assets as assets
from game_settings import g_vars

class BasicTile(sprite.Sprite):
    def __init__(self, gamemap, location):
        sprite.Sprite.__init__(self, self.groups) # Add self to group
        # map
        self.gamemap = gamemap
        self.location = location
        # pathing
        self.passable = g_vars["Tile"]["Basic"]["Passable"] == 1
        self.movement_straight = g_vars["Tile"]["Basic"]["MovementStraight"]
        self.movement_diagonal = g_vars["Tile"]["Basic"]["MovementDiagonal"]
        # graphic
        #self.image = assets.LoadSprite("unicorn.jpg")
        self.image = Surface((g_vars["Game"]["TileSize"], g_vars["Game"]["TileSize"]))
        self.image.fill(g_vars["Game"]["TileColors"][self.tile_color])
        self.rect = self.image.get_rect()
        self.rect.x = location[0] * g_vars["Game"]["TileSize"]
        self.rect.y = location[1] * g_vars["Game"]["TileSize"]

        # Resource
        self.resource_list = []

    def add_resource(self, resource, amount=1):
        for x in range(amount):
            y1 = self.location[1]
            x1 = self.location[0]
            new_resource = resource(self.gamemap, (x1, y1))
            self.resource_list.append(new_resource)

    def has_resources_remaining(self):
        return len(self.resource_list) > 0

    def deduct_resource(self):
        pass

class Fog(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_fog
        self.tile_color = "Fog"
        BasicTile.__init__(self, gamemap, location)
        #self.passable = g_vars["Tile"]["Fog"]["Passable"] == "1"

class Forest(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "Forest"
        BasicTile.__init__(self, gamemap, location)
        self.passable = g_vars["Tile"]["Forest"]["Passable"] == 1
        self.movement_straight = g_vars["Tile"]["Forest"]["MovementStraight"]
        self.movement_diagonal = g_vars["Tile"]["Forest"]["MovementDiagonal"]

class Ground(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "Ground"
        BasicTile.__init__(self, gamemap, location)
        self.passable = g_vars["Tile"]["Ground"]["Passable"] == 1
        self.movement_straight = g_vars["Tile"]["Ground"]["MovementStraight"]
        self.movement_diagonal = g_vars["Tile"]["Ground"]["MovementDiagonal"]

class Water(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "Water"
        BasicTile.__init__(self, gamemap, location)
        self.passable = g_vars["Tile"]["Water"]["Passable"] == 1

class Bog(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "Bog"
        BasicTile.__init__(self, gamemap, location)
        self.passable = g_vars["Tile"]["Bog"]["Passable"] == 1
        self.movement_straight = g_vars["Tile"]["Bog"]["MovementStraight"]
        self.movement_diagonal = g_vars["Tile"]["Bog"]["MovementDiagonal"]

class Mountain(BasicTile):
    def __init__(self, gamemap, location):
        self.groups = gamemap.sprite_group_background
        self.tile_color = "Mountain"
        BasicTile.__init__(self, gamemap, location)
        self.passable = g_vars["Tile"]["Mountain"]["Passable"] == 1