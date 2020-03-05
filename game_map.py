import pygame as pg
from os import path

import game_settings as settings
import game_assets as assets
import game_tiles as tiles
import algorithms as alg

class GameMap:

    def __init__(self):
        self.sprite_group_background = pg.sprite.Group()
        self.sprite_group_fog = pg.sprite.Group()
        self.sprite_group_entities = pg.sprite.Group()
        self.unpassable_tiles = []
        self.cleared_fog = []
        self.weighted_graph = None
        self.camera = None
        self.map_width = 0
        self.map_height = 0

        self.draw_fog = False

    def load_map_template(self, template_name):
        # Open map template
        with open(path.join(assets.map_folder, template_name), "rt") as f:

            # Construct tiles from map file
            for y, row in enumerate(f):
                row = row.strip("\n")
                # count map height
                self.map_height += 1
                self.map_width = 0

                for x, tile in enumerate(row):
                    # count map width (lazy mf)
                    self.map_width += 1

                    # fog is everywhere
                    tiles.Fog(self, (x, y))
                    
                    if tile == "T": # Forest
                        tiles.Forest(self, (x, y))
                    
                    elif tile == "V": # Water
                        tiles.Water(self, (x, y))
                        self.unpassable_tiles.append((x, y))
                        
                    elif tile == "G": # Bog
                        tiles.Bog(self, (x, y))
                       
                    elif tile == "B": # Mountain
                        tiles.Mountain(self, (x, y))
                        self.unpassable_tiles.append((x, y))
                    
                    elif tile == "M": # Ground
                        tiles.Ground(self, (x, y))

        settings.MAP_WIDTH = self.map_width * settings.TILE_SIZE
        settings.MAP_HEIGHT = self.map_height * settings.TILE_SIZE

        self.weighted_graph = alg.WeightedGraph(self)
        self.camera = Camera(settings.MAP_WIDTH, settings.MAP_HEIGHT)

    def update(self):
        self.sprite_group_background.update()
        self.sprite_group_entities.update()
        self.sprite_group_fog.update()

    def draw(self, screen):
        for sprite in self.sprite_group_background:
            # apply offset to camera to all sprites 
            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.sprite_group_entities:
            screen.blit(sprite.image, self.camera.apply(sprite))

        if self.draw_fog:
            for sprite in self.sprite_group_fog:
                screen.blit(sprite.image, self.camera.apply(sprite))

    def get_background_tile(self, cords):
        for tile in self.sprite_group_background:
            if cords == (tile.location[0], tile.location[1]):
                return tile
    
    def get_fog_tile(self, cords):
        for tile in self.sprite_group_fog:
            if cords == (tile.location[0], tile.location[1]):
                return tile

    def remove_tile(self, tile):
        pg.sprite.Sprite.remove(tile, tile.groups)
    
    def clear_fog_area(self, start, stop):
        (x1, y1), (x2, y2) = start, stop
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                # get fog tile if it exists
                tile = self.get_fog_tile((x, y))
                if tile:
                    self.cleared_fog.append((x, y))
                    self.remove_tile(tile)

    def get_path(self, start, goal):
        return alg.Astar(self.weighted_graph, goal, start)

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def move(self, dx=0, dy=0):
        self.x += dx * int(settings.TILE_SIZE)
        self.y += dy * int(settings.TILE_SIZE)
        self.camera = pg.Rect(-self.x, -self.y, self.width, self.height)

    