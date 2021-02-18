#import math
#from random import randint

from os import W_OK
from GOAP.transform import Position
import pygame as pg

#import ai_state as states
import game_entities as entities
import game_map as gamemap
import game_time as time
from game_settings import g_vars

from GOAP.Agents.worker import Worker
from GOAP.Agents.explorer import Explorer
from GOAP.Agents.artisan import Artisan, Profession
from GOAP.Agents.refinery import Refinery
from GOAP.Agents.player import Player

# TODO visible resources / resource piles
# TODO explorer search bias
# TODO better production (ex. when queuing artisan it should produce one)

class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption(g_vars["Game"]["Title"])
        self.map = gamemap.GameMap()
        self.speed = 100
        self.paused = False
        self.draw_grid = False
        self.draw_ui = True
        self.draw_ui_tasks = False
        self.draw_ui_resources = False
        self.draw_ui_entities = False
        self.agents = []

    # Specify a gamemap to use
    def set_map(self, map_name):
        # load map
        self.map.load_map_template(map_name)
        # Updates screen size to loaded map
        self.screen = pg.display.set_mode((g_vars["Game"]["ScreenWidth"], g_vars["Game"]["ScreenHeight"]))

    def enable_GOAP_ai(self):
        #agents.append(DragonKeeper(dragon))
        #agents.append(dragon)
        player = Player(self.map, Position(3, 3))

        builder = Artisan()
        refiner = Artisan()
        builder.profession = Profession.Builder
        refiner.profession = Profession.Refiner
        player.add_unit(builder)
        player.add_unit(refiner)

        refinery = Refinery()
        # refinery.on_fetched("Logs")
        # refinery.on_fetched("Logs")
        player.add_structure(refinery)
        
        player.add_unit(Worker())
        player.add_unit(Worker())
        player.add_unit(Worker())
        player.add_unit(Worker())
        player.add_unit(Worker())
        # player.add_unit(Explorer())
        self.agents.append(player)

    def set_fog_visibility(self, value):
        self.map.draw_fog = value

    def run(self):
        self.running = True

        for agent in self.agents:
            agent.start_agent()

        while (self.running):
            #time.clock.update(g_vars["Game"]["FPS"], self.speed)
            time.clock.update(60)    
            self.update()
            self.draw()
            self.events()

    def update(self):
        # send screen to map for blit
        if not self.paused:
            self.map.update()

        # AI
        for agent in self.agents:
            agent.update()

        # catch inputs
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            pg.event.post(pg.event.Event(pg.QUIT))

        if keystate[pg.K_TAB]:
            self.map.draw_fog = not self.map.draw_fog

        if keystate[pg.K_SPACE]:
            self.paused = not self.paused

        if keystate[pg.K_KP_PLUS]:
            self.speed -= 100
            if self.speed <= 0:
                self.speed = 10
        if keystate[pg.K_KP_MINUS]:
            self.speed += 100

        if keystate[pg.K_1]:
            self.draw_ui_tasks = not self.draw_ui_tasks
        if keystate[pg.K_2]:
            self.draw_ui_resources = not self.draw_ui_resources
        if keystate[pg.K_3]:
            self.draw_ui_entities = not self.draw_ui_entities
        if keystate[pg.K_g]:
            self.draw_grid = not self.draw_grid
        if keystate[pg.K_q]:
            self.draw_ui = not self.draw_ui
        if keystate[pg.K_w]:
            self.map.camera.move(dy=-1)
        if keystate[pg.K_s]:
            self.map.camera.move(dy=1)
        if keystate[pg.K_a]:
            self.map.camera.move(dx=-1)
        if keystate[pg.K_d]:
            self.map.camera.move(dx=1)

    def draw_grid_overlay(self):
        for x in range(0, self.map.width, g_vars["Game"]["TileSize"]):
            pg.draw.line(self.screen, g_vars["Game"]["Colors"]["LightGray"], (x, 0), (x, self.map.height))
        for y in range(0, self.map.height, g_vars["Game"]["TileSize"]):
            pg.draw.line(self.screen, g_vars["Game"]["Colors"]["LightGray"], (0, y), (self.map.width, y))

    def draw(self):
        # Background
        self.screen.fill(g_vars["Game"]["Colors"]["LightGray"])
        # Tiles
        self.map.draw(self.screen)
        # Overlay
        if self.draw_grid:
            self.draw_grid_overlay()
        # Flip
        pg.display.flip()

    def events(self):
        # catch events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
