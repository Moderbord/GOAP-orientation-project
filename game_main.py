import math
from random import randint

import pygame as pg
import thorpy

import ai_state as states
import game_entities as entities
import game_map as gamemap
import game_time as time
import message_dispatcher as dispatcher
import player_ai as ai
from game_settings import g_vars

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
        self.ai_player.resource_map.update(self.map.discover_fog_area((1, 1), (50, 50)))
        self.ai_player.append_goal(["Unit", "Soldier", 20])

        for x in range(0, 50):
            worker = entities.UnitWorker(self.ai_player)
            worker.spawn()

    def init_thorpy(self):
        res_trees = thorpy.OneLineText("Trees: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.Tree)))))
        self.box = thorpy.Box(elements=[res_trees])
        self.box_u = thorpy.Box(elements=[res_trees])
        self.box_r = thorpy.Box(elements=[res_trees])
        #we regroup all elements on a menu, even if we do not launch the menu
        menu = thorpy.Menu([self.box, self.box_u])
        #important : set the screen as surface for all elements
        for element in menu.get_population():
            element.surface = self.screen
        #use the elements normally...
        self.box.set_topleft((0, 0))

    def update_thorpy(self):
        # tasks
        if self.draw_ui_tasks:
            goal = thorpy.MultilineText(str(self.ai_player.current_goal), (220, 50))
            task = thorpy.MultilineText(str(self.ai_player.current_task), (220, 50))
            task_list = thorpy.MultilineText(str(self.ai_player.task_list.elements), (220, 600))
            self.box = thorpy.Box(elements=[goal, task, task_list])
            self.box.blit()
            self.box.update()

        # resources
        if self.draw_ui_resources:
            resources = thorpy.MultilineText("Trees: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.Tree))))
            + "          Coal: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.Coal))))
            + "          IronOre: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.IronOre))))
            + "          IronBar: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.IronBar))))
            + "          Swords: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.Sword)))), (600, 30))
            self.box_r = thorpy.Box(elements=[resources])
            self.box_r.set_topleft((230, 0))
            self.box_r.blit()
            self.box_r.update()

        # units
        if self.draw_ui_entities:
            units = thorpy.MultilineText("Workers: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.UnitWorker))))
            + "          Explorers: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.UnitExplorer))))
            + "          Artisans: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.UnitArtisan))))
            + "          Soldiers: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.UnitSoldier)))), (500, 30))
            self.box_u = thorpy.Box(elements=[units])
            self.box_u.set_topleft((230, 40))
            self.box_u.blit()
            self.box_u.update()

    def enable_fog(self):
        self.map.draw_fog = True

    def run(self):
        self.running = True
        while (self.running):
            time.delta_time = time.clock.tick(g_vars["Game"]["FPS"]) / self.speed
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
        # UI
        if self.draw_ui:
            self.update_thorpy()
        # Flip
        pg.display.flip()

    def events(self):
        # catch events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
