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
        self.paused = False
        self.ai_player = None
        self.menu = None

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
        self.ai_player.append_goal(["Unit", "Soldier", 5])

        for x in range(0, 50):
            worker = entities.UnitWorker(self.ai_player)
            worker.spawn()
            self.ai_player.add_entity(worker)

    def init_thorpy(self):
        res_trees = thorpy.OneLineText("Trees: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.Tree)))))
        self.box = thorpy.Box(elements=[res_trees])
        #we regroup all elements on a menu, even if we do not launch the menu
        self.menu = thorpy.Menu(self.box)
        #important : set the screen as surface for all elements
        for element in self.menu.get_population():
            element.surface = self.screen
        #use the elements normally...
        self.box.set_topleft((0, 0))

    def update_thorpy(self):
        res_trees = thorpy.OneLineText("Trees: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.Tree)))))
        res_coal = thorpy.OneLineText("Coal: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.Coal)))))
        res_iron_ore = thorpy.OneLineText("IronOre: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.IronOre)))))
        res_iron_bar = thorpy.OneLineText("IronBar: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.IronBar)))))
        res_swords = thorpy.OneLineText("Swords: " + str(len(self.ai_player.entities_where(lambda e: isinstance(e, entities.Sword)))))
        goal = thorpy.MultilineText(str(self.ai_player.current_goal), (300, 50))
        task = thorpy.MultilineText(str(self.ai_player.current_task), (300, 50))
        task_list = thorpy.MultilineText(str(self.ai_player.task_list.elements), (220, 600))
        self.box = thorpy.Box(elements=[res_trees, res_coal, res_iron_ore, res_iron_bar, res_swords, goal, task, task_list])
        self.box.blit()
        self.box.update()

    def enable_fog(self):
        self.map.draw_fog = True

    def run(self):
        self.running = True
        while (self.running):
            time.delta_time = time.clock.tick(g_vars["Game"]["FPS"]) / 100
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

        if keystate[pg.K_q]:
            test = self.ai_player.entities_where(lambda x: (x.is_idle == True))
            for x in test:
                print (x)
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
        #self.draw_grid_overlay()
        
        self.update_thorpy()
        # Flip
        pg.display.flip()

    def events(self):
        # catch events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            # if event.type == pg.MOUSEBUTTONUP:
            #     mouse = pg.mouse.get_pos()
            #     x = max(math.floor((mouse[0]) / g_vars["Game"]["TileSize"]), 0)
            #     y = max(math.floor((mouse[1]) / g_vars["Game"]["TileSize"]), 0)
            #     print(str(x) + ", " + str(y))
            #     if self.ai_player:
            #         self.ai_player.print_unit_at_location((x, y))
            if self.menu:
                self.menu.react(event)
