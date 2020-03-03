from os import path
from pygame import sprite
import random

import game_settings as settings
import game_assets as assets
import game_tiles as tiles
# import algorithms as alg

class GameMap:

    def __init__(self):
        self.sprite_group_all = sprite.Group()
        self.unpassable_tiles = []
        self.map_width = 0
        self.map_height = 0

    def load_map_template(self, template_name):
        # Open map template
        with open(path.join(assets.map_folder, template_name), "rt") as f:

            # Construct tiles from map file
            for y, row in enumerate(f):
                # count map height
                self.map_height += 1
                self.map_width = 0

                for x, tile in enumerate(row):
                    # count map width (lazy mf)
                    self.map_width += 1
                    
                    if tile == "T": # Forest
                        tiles.Forest(self, x, y)
                    
                    elif tile == "V": # Water
                        tiles.Water(self, x, y)
                        self.unpassable_tiles.append((x, y))
                        
                    elif tile == "G": # Bog
                        tiles.Bog(self, x, y)
                       
                    elif tile == "B": # Mountain
                        tiles.Mountain(self, x, y)
                        self.unpassable_tiles.append((x, y))
                    
                    elif tile == "M": # Ground
                        tiles.Ground(self, x, y)

        settings.MAP_WIDTH = self.map_width * settings.TILE_SIZE
        settings.MAP_HEIGHT = self.map_height * settings.TILE_SIZE

    def update(self):
        self.sprite_group_all.update()

    def draw(self, screen):
        self.sprite_group_all.draw(screen)

    # def astar_cost(self):
    #     path, cost = alg.Astar(alg.WeightedGraph(self), self.custom_start, self.custom_goal)
    #     return cost
    