import pygame as pg
from os import path
from random import randint

import game_assets as assets
import game_tiles as tiles
import game_entities as entities
import algorithms as alg
from game_settings import g_vars

class GameMap:

    def __init__(self):
        self.sprite_group_background = pg.sprite.Group()
        self.sprite_group_fog = pg.sprite.Group()
        self.sprite_group_units = pg.sprite.Group()
        self.sprite_group_structures = pg.sprite.Group()
        self.sprite_group_resources = pg.sprite.Group()
        self.tile_data = {}
        self.fog_data = {}
        self.occupied_tiles = {}
        self.unpassable_tiles = []
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
                    self.fog_data[(x, y)] = tiles.Fog(self, (x, y))
                    
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

        for i in range(0, 360):
            tile = self.get_random_background_tile()
            while not tile.passable:
                tile = self.get_random_background_tile()
            tile.add_resource(entities.WildIronOre, 1)

        self.width = self.tile_width * g_vars["Game"]["TileSize"]
        self.height = self.tile_height * g_vars["Game"]["TileSize"]

        self.weighted_graph = alg.WeightedGraph(self)
        self.camera = Camera(self.width, self.height)

    def update(self):
        self.sprite_group_background.update()
        self.sprite_group_resources.update()
        self.sprite_group_structures.update()
        self.sprite_group_units.update()
        self.sprite_group_fog.update()

    def draw(self, screen):
        # loop through all tiles
        for x in range(0, self.tile_width):
            for y in range(0, self.tile_height):

                # check if fog
                if self.draw_fog:
                    tile = self.get_fog_tile((x, y))
                    # draw fog if it exists
                    if tile:
                        screen.blit(tile.image, self.camera.apply(tile))
                        continue
                
                # draw background
                tile = self.get_background_tile((x, y))
                screen.blit(tile.image, self.camera.apply(tile))
                # draw resource if any
                if tile.has_resources_remaining():
                    for resource in tile.resource_list:
                        screen.blit(resource.image, self.camera.apply(resource))

        for sprite in self.sprite_group_structures:
            if sprite.is_visible:
                screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.sprite_group_units:
            if sprite.is_visible:
                screen.blit(sprite.image, self.camera.apply(sprite))

    def get_background_tile(self, cords):
        return self.tile_data[cords]

    def get_random_background_tile(self):
        x, y = randint(0, self.tile_width - 1), randint(0, self.tile_height - 1)
        return self.tile_data[(x, y)]

    def get_fog_tile(self, cords):
        return self.fog_data.get(cords, False)

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
                    del self.fog_data[(x, y)]
                    self.remove_tile(tile)
                    # add to discovered map
                    discovered_tile = self.get_background_tile((x, y))
                    if discovered_tile.has_resources_remaining():
                        discovered_resources[(x, y)] = discovered_tile
        return discovered_resources

    def get_buildable_area(self, center, radius):
        buildable_tiles = []
        (x1, y1) = center
        # scan specified area
        for x in range(abs(x1 - radius), x1 + radius + 1):
            # map boundaries
            if x >= self.tile_width:
                return None
            for y in range(abs(y1 - radius), y1 + radius + 1):
                # map boundaries
                if y >= self.tile_height:
                    return None
                # get tile and check availability
                tile = self.get_background_tile((x, y))
                if isinstance(tile, tiles.Ground) and self.location_is_discovered(tile.location) and not self.tile_is_occupied(tile):
                    buildable_tiles.append(tile)
        return buildable_tiles

    def occupy_tile(self, tile):
        self.occupied_tiles[tile.location] = True

    def tile_is_occupied(self, tile):
        return self.occupied_tiles.get(tile.location, False)

    def location_is_discovered(self, location):
        return not self.fog_data.get(location, False)

    def get_path(self, start, goal, filter_function):
        return alg.Astar(self.weighted_graph, goal, start, filter_function)

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

    