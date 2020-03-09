import pygame as pg
from os import path

import game_assets as assets
import game_tiles as tiles
import game_entities as entities
import algorithms as alg
from game_settings import g_vars

class GameMap:

    def __init__(self):
        self.sprite_group_background = pg.sprite.Group()
        self.sprite_group_fog = pg.sprite.Group()
        self.sprite_group_entities = pg.sprite.Group()
        self.sprite_group_resources = pg.sprite.Group()
        self.tile_data = {}
        self.unpassable_tiles = []
        self.cleared_fog = []
        self.weighted_graph = None
        self.camera = None
        self.width = 0
        self.height = 0
        self.tile_width = 0
        self.tile_height = 0

        self.draw_fog = False

    def load_map_template(self, template_name):
        # Open map template
        with open(path.join(assets.map_folder, template_name), "rt") as f:

            # Construct tiles from map file
            for y, row in enumerate(f):
                row = row.strip("\n")
                # count map height
                self.tile_height += 1
                self.tile_width = 0

                for x, tile in enumerate(row):
                    # count map width (lazy mf)
                    self.tile_width += 1

                    # fog is everywhere
                    tiles.Fog(self, (x, y))
                    new_tile = None

                    if tile == "T": # Forest
                        new_tile = tiles.Forest(self, (x, y))
                        new_tile.add_resource(entities.WildTree, 5)

                    elif tile == "V": # Water
                        new_tile = tiles.Water(self, (x, y))
                        self.unpassable_tiles.append((x, y))
                        
                    elif tile == "G": # Bog
                        new_tile = tiles.Bog(self, (x, y))
                       
                    elif tile == "B": # Mountain
                        new_tile = tiles.Mountain(self, (x, y))
                        self.unpassable_tiles.append((x, y))
                    
                    elif tile == "M": # Ground
                        new_tile = tiles.Ground(self, (x, y))
                    
                    self.tile_data[(x, y)] = new_tile

        self.width = self.tile_width * g_vars["Game"]["TileSize"]
        self.height = self.tile_height * g_vars["Game"]["TileSize"]

        self.weighted_graph = alg.WeightedGraph(self)
        self.camera = Camera(self.width, self.height)

    def update(self):
        self.sprite_group_background.update()
        self.sprite_group_resources.update()
        self.sprite_group_entities.update()
        self.sprite_group_fog.update()

    def draw(self, screen):
        for sprite in self.sprite_group_background:
            # apply offset to camera to all sprites 
            screen.blit(sprite.image, self.camera.apply(sprite))
        
        for sprite in self.sprite_group_resources:
            screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.sprite_group_entities:
            if sprite.is_visible:
                screen.blit(sprite.image, self.camera.apply(sprite))

        if self.draw_fog:
            for sprite in self.sprite_group_fog:
                screen.blit(sprite.image, self.camera.apply(sprite))

    def get_background_tile(self, cords):
        return self.tile_data[cords]
        # for tile in self.sprite_group_background:
        #     if cords == (tile.location[0], tile.location[1]):
        #         return tile
    
    def get_fog_tile(self, cords):
        for tile in self.sprite_group_fog:
            if cords == (tile.location[0], tile.location[1]):
                return tile

    def remove_tile(self, tile):
        pg.sprite.Sprite.remove(tile, tile.groups)
    
    def discover_fog_area(self, start, stop):
        discovered_resources = {}
        (x1, y1), (x2, y2) = start, stop
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                # get fog tile if it exists
                tile = self.get_fog_tile((x, y))
                if tile:
                    self.cleared_fog.append((x, y))
                    self.remove_tile(tile)
                    # add to discovered map
                    discovered_tile = self.get_background_tile((x, y))
                    if discovered_tile.has_resources_remaining():
                        discovered_resources[(x, y)] = discovered_tile.resource_list
        return discovered_resources

    def get_buildable_area(self, center, radius):
        buildable_tiles = []
        (x1, y1) = center
        for x in range(x1 - radius, x1 + radius + 1):
            for y in range(y1 - radius, y1 + radius + 1):
                tile = self.get_background_tile((x, y))
                if isinstance(tile, tiles.Ground):
                    buildable_tiles.append(tile)
        return buildable_tiles

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
        self.x += dx * int(g_vars["Game"]["TileSize"])
        self.y += dy * int(g_vars["Game"]["TileSize"])
        self.camera = pg.Rect(-self.x, -self.y, self.width, self.height)

    