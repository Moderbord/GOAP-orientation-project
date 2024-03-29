from random import randint

from GOAP.transform import Position
import pygame as pg

import game_time as time
from game_settings import g_vars
from game_server import g_map
from camera import camera

from GOAP.Agents.artisan import Profession
from GOAP2.resource_sensor import ResourceSensor
from GOAP2.goap_controller import GOAPController
from GOAP2.working_memory import WorkingMemoryFact, FactType
from GOAP2.units.worker import Worker
from GOAP2.units.artisan import Artisan
from GOAP2.units.soldier import Soldier
from GOAP2.structures.refinery import Refinery
from GOAP2.structures.camp import Camp
from GOAP2.structures.encampment import Encampment
from GOAP2.structures.smithy import Smithy
from GOAP2.structures.smelter import Smelter
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
        for x in range(0, 50):
            worker = Worker()
            agent = GOAPController()
            agent.setup(worker)
            agent.enable_navigation()
            agent.enable_targeting()
            agent.enable_sensors()
            agent.attach_sensor(ResourceSensor())

            fact_x = WorkingMemoryFact()
            res_pos = g_player.get_resource_drop_off_loc()
            fact_x.set_pos(res_pos, 0.5).set_ftype(FactType.Delivery)
            agent.working_memory.create_fact(fact_x)

            agent.blackboard.set_position(Position(2, 2))
            g_player.add_unit(agent)
        ##

        refinery = Refinery()
        agent = GOAPController()
        agent.setup(refinery)
        agent.blackboard.set_position(Position(4, 5))
        agent.blackboard.set_required_artisan(Profession.Refiner)
        g_player.add_structure(agent)

        camp = Camp()
        agent = GOAPController()
        agent.setup(camp)
        agent.blackboard.set_is_built(True)
        agent.blackboard.set_position(Position(2, 2))
        g_player.add_structure(agent)

        smelter = Smelter()
        agent = GOAPController()
        agent.setup(smelter)
        agent.blackboard.set_position(Position(4, 1))
        agent.blackboard.set_required_artisan(Profession.Metallurgist)
        g_player.add_structure(agent)

        smithy = Smithy()
        agent = GOAPController()
        agent.setup(smithy)
        agent.blackboard.set_position(Position(1, 4))
        agent.blackboard.set_required_artisan(Profession.Smith)
        g_player.add_structure(agent)

        encampment = Encampment()
        agent = GOAPController()
        agent.setup(encampment)
        agent.blackboard.set_position(Position(8, 1))
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

            self.running = len([u for u in g_player.units if type(u.entity).__name__ == "Soldier"]) < 20

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
        # remove
        if len(g_player.pending_deletes) > 0:
            for id in g_player.pending_deletes:
                for unit in g_player.units:
                    if unit.id == id:
                        g_player.units.remove(unit)
                        break
            g_player.pending_deletes.clear()
        # create
        if len(g_player.pending_creates) > 0:
            for new_unit in g_player.pending_creates:
                (entity, position) = new_unit
                unit = None
                if entity == "Artisan":
                    unit = Artisan()
                elif entity == "Explorer":
                    pass
                elif entity == "Soldier":
                    unit = Soldier()
                elif entity == "Worker":
                    pass
                agent = GOAPController()
                agent.setup(unit)
                agent.blackboard.set_position(position)
                agent.enable_navigation()
                agent.enable_targeting()
                g_player.add_unit(agent)

            g_player.pending_creates.clear()

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

    