from random import randint

from GOAP.transform import Position
import pygame as pg

import game_time as time
from game_settings import g_vars
from game_server import g_map
from camera import camera

from GOAP2.resource_sensor import ResourceSensor
from GOAP2.goap_controller import GOAPController
from GOAP2.working_memory import WorkingMemoryFact, FactType
from GOAP2.units.worker import Worker
from GOAP2.structures.refinery import Refinery
from GOAP2.player import g_player

class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption(g_vars["Game"]["Title"])
        self.map = None
        self.speed = 5
        self.paused = False
        self.draw_grid = False
        self.agents = []

    # Specify a gamemap to use
    def set_map(self, map_name):
        # load map
        #self.map.load_map_template(map_name)
        self.map = g_map
        # Updates screen size to loaded map
        self.screen = pg.display.set_mode((g_vars["Game"]["ScreenWidth"], g_vars["Game"]["ScreenHeight"]))

    def set_fog_visibility(self, value):
        self.map.draw_fog = value

    def run(self):
        self.running = True

        ##
        for x in range(0, 1):
            worker = Worker()
            agent = GOAPController()
            agent.setup(worker)
            agent.enable_navigation()
            agent.enable_targeting()
            agent.enable_sensors()
            agent.attach_sensor(ResourceSensor())

            fact_x = WorkingMemoryFact()
            fact_x.set_pos(Position(2, 2), 0.5).set_ftype(FactType.Delivery)
            agent.working_memory.create_fact(fact_x)

            g_player.add_unit(agent)
        ##

        refinery = Refinery()
        agent = GOAPController()
        agent.setup(refinery)
        agent.enable_sensors()
        g_player.add_structure(agent)

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
        print("------------------- BARF FORTRESS 3.0 --------------------")
        print("Elapsed time: " + str(t_end - t_start) + " ms")
        print("Frames: " + str(frames))
        print("Update time: " + str(update_time) + " ms")
        print("Update efficiency: " + str(update_time / frames) + " ms/frame")
        print("Draw time: " + str(draw_time) + " ms")
        print("Draw efficiency: " + str(draw_time / frames) + " ms/frame")

    def update(self):
        g_player.update()
            
        # catch inputs
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            pg.event.post(pg.event.Event(pg.QUIT))

        if keystate[pg.K_TAB]:
            self.map.draw_fog = not self.map.draw_fog

        if keystate[pg.K_SPACE]:
            self.paused = not self.paused

        if keystate[pg.K_KP_PLUS]:
            self.speed += 5
        if keystate[pg.K_KP_MINUS]:
            self.speed -= 5
            if self.speed <= 0:
                self.speed = 1

        # if keystate[pg.K_w]:
        #     self.agents[0].y -= 1
        # if keystate[pg.K_s]:
        #     self.agents[0].y += 1
        # if keystate[pg.K_a]:
        #     self.agents[0].x -= 1
        # if keystate[pg.K_d]:
        #     self.agents[0].x += 1
        if keystate[pg.K_w]:
            camera.move(dy=-1)
        if keystate[pg.K_s]:
            camera.move(dy=1)
        if keystate[pg.K_a]:
            camera.move(dx=-1)
        if keystate[pg.K_d]:
            camera.move(dx=1)

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

        # Agents
        g_player.render(self.screen, camera)

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

    