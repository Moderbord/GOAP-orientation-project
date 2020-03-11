from random import randint
import math
import pygame as pg

import game_map as gamemap
import player_ai as ai
import game_entities as entities
import ai_state as states
import game_time as time
import message_dispatcher as dispatcher
from game_settings import g_vars

# TODO visible resources / resource piles
# TODO explorer search bias
# TODO better production (ex. when queuing artisan it should produce one)

class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption(g_vars["Game"]["Title"])
        self.map = gamemap.GameMap()
        self.paused = False
        self.ai_player = None

    # Specify a gamemap to use
    def set_map(self, map_name):
        # load map
        self.map.load_map_template(map_name)
        # Updates screen size to loaded map
        self.screen = pg.display.set_mode((g_vars["Game"]["ScreenWidth"], g_vars["Game"]["ScreenHeight"]))

    def enable_explorer(self):
        #self.explorer = entities.UnitExplorer(self.map, (2, 2))
        self.map.discover_fog_area((1, 1), (3, 3))

    def enable_ai(self):
        self.ai_player = ai.AI(self.map, (2, 2))
        self.map.discover_fog_area((1, 1), (3, 3))
        self.ai_player.append_goal(["Unit", "Soldier", 1])

        for x in range(0, 50):
            worker = entities.UnitWorker(self.ai_player)
            worker.spawn()
            self.ai_player.add_unit(worker)
            self.ai_player.worker_units.append(worker)

    def enable_fog(self):
        self.map.draw_fog = True

    def run(self):
        self.running = True
        while (self.running):
            time.delta_time = time.clock.tick(g_vars["Game"]["FPS"]) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        # send screen to map for blit
        if not self.paused:
            self.map.update()

        # AI
        if self.ai_player and not self.paused:
            self.ai_player.update()

        # catch inputs
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            pg.event.post(pg.event.Event(pg.QUIT))

        if keystate[pg.K_TAB]:
            self.map.draw_fog = not self.map.draw_fog

        if keystate[pg.K_SPACE]:
            self.paused = not self.paused

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
        # AI
        self.ai_player.draw(self.screen)
        # Overlay
        #self.draw_grid_overlay()
        # Flip
        pg.display.flip()

    def events(self):
        # catch events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos()
                x = max(math.floor((mouse[0]) / g_vars["Game"]["TileSize"]), 0)
                y = max(math.floor((mouse[1]) / g_vars["Game"]["TileSize"]), 0)
                print(str(x) + ", " + str(y))
                if self.ai_player:
                    self.ai_player.print_unit_at_location((x, y))
            
                
