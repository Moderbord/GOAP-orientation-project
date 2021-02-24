import pygame as pg

import game_map as gamemap
import game_time as time
from game_settings import g_vars
from game_server import g_map

from GOAP.Agents.worker import Worker
from GOAP.Agents.refinery import Refinery
from GOAP.Agents.encampment import Encampment
from GOAP.Agents.smithy import Smithy
from GOAP.Agents.smelter import Smelter
from GOAP.Agents.camp import Camp
from GOAP.Agents.player import Player
from GOAP.transform import Position

# Dragon 
from GOAP.Agents.dragon_keeper import DragonKeeper
from GOAP.Agents.dragon import Dragon

class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption(g_vars["Game"]["Title"])
        self.map = gamemap.GameMap()
        self.speed = 20
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
        #self.map.load_map_template(map_name)
        self.map = g_map
        # Updates screen size to loaded map
        self.screen = pg.display.set_mode((g_vars["Game"]["ScreenWidth"], g_vars["Game"]["ScreenHeight"]))

    def enable_dragon_scenario(self):
        dragon = Dragon()
        self.agents.append(DragonKeeper(dragon))
        self.agents.append(dragon)

    def enable_GOAP_ai(self):
        player = Player(self.map, Position(3, 3))

        # builder = Artisan()
        # refiner = Artisan()
        # builder.profession = Profession.Builder
        # refiner.profession = Profession.Refiner
        # player.add_unit(builder)
        # player.add_unit(refiner)

        # refinery.on_fetched("Logs")
        # refinery.on_fetched("Logs")
        player.add_structure(Refinery())
        player.add_structure(Camp())
        player.add_structure(Encampment())
        player.add_structure(Smithy())
        player.add_structure(Smelter())

        for x in range(50):
            player.add_unit(Worker())
        
        # player.add_unit(Explorer())
        self.agents.append(player)

    def set_fog_visibility(self, value):
        self.map.draw_fog = value

    def run(self):
        self.running = True

        for agent in self.agents:
            agent.start_agent()

            # dragon scenario
            agent.groups = g_map.sprite_group_units
            agent.start_actor()

        frames = 0
        update_time = 0.0
        draw_time = 0.0

        t_start = time.now()

        while (self.running):
            #time.clock.update(g_vars["Game"]["FPS"], self.speed)
            time.clock.update(60, self.speed)  
            frames += 1
            t1 = time.now()  
            self.update()
            t2 = time.now()
            update_time += t2 - t1
            self.draw()
            t3 = time.now()
            draw_time += t3 - t2
            self.events()

            #self.running = self.agents[0].count_units("Soldier") < 20

        t_end = time.now()

        print("")
        print("------------------- BARF FORTRESS 2.0 --------------------")
        print("Elapsed time: " + str(t_end - t_start) + " ms")
        print("Frames: " + str(frames))
        print("Update time: " + str(update_time) + " ms")
        print("Update efficiency: " + str(update_time / frames) + " ms/frame")
        print("Draw time: " + str(draw_time) + " ms")
        print("Draw efficiency: " + str(draw_time / frames) + " ms/frame")

    def update(self):
        # send screen to map for blit
        # if not self.paused:
        #     self.map.update()

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
