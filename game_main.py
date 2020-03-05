from random import randint
import pygame as pg

import algorithms as alg
import game_settings as settings
import game_map as gamemap
import game_tiles as tiles
import game_entities as entities

class Game:

    def __init__(self):
        pg.init()
        pg.display.set_caption(settings.TITLE)
        self.clock = pg.time.Clock()
        self.map = gamemap.GameMap()

    # Specify a gamemap to use
    def set_map(self, map_name):
        # load map
        self.map.load_map_template(map_name)
        # Updates screen size to loaded map
        self.screen = pg.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def enable_explorer(self):
        self.explorer = entities.UnitExplorer(self.map, (2, 2))
        self.map.clear_fog_area((1, 1), (3, 3))


    def enable_fog(self):
        self.map.draw_fog = True

    def run(self):
        self.running = True
        while (self.running):
            self.dt = self.clock.tick(settings.FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        # send screen to map for blit
        self.map.update()

        # catch inputs
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            pg.event.post(pg.event.Event(pg.QUIT))

        if keystate[pg.K_TAB]:
            self.map.draw_fog = not self.map.draw_fog

        if keystate[pg.K_SPACE]:
            path = self.map.get_path(self.explorer.location, (randint(0, self.map.map_width - 1), (randint(0, self.map.map_height - 1))))
            if path:
                self.explorer.set_path(path)

        if keystate[pg.K_w]:
            self.map.camera.move(dy=-1)
        if keystate[pg.K_s]:
            self.map.camera.move(dy=1)
        if keystate[pg.K_a]:
            self.map.camera.move(dx=-1)
        if keystate[pg.K_d]:
            self.map.camera.move(dx=1)

        if (self.explorer):
            if keystate[pg.K_UP]:
                self.explorer.move(dy=-1)
            if keystate[pg.K_DOWN]:
                self.explorer.move(dy=1)
            if keystate[pg.K_LEFT]:
                self.explorer.move(dx=-1)
            if keystate[pg.K_RIGHT]:
                self.explorer.move(dx=1)

    def draw_grid_overlay(self):
        for x in range(0, settings.MAP_WIDTH, settings.TILE_SIZE):
            pg.draw.line(self.screen, settings.COLOR["LIGHTGRAY"], (x, 0), (x, settings.MAP_HEIGHT))
        for y in range(0, settings.MAP_HEIGHT, settings.TILE_SIZE):
            pg.draw.line(self.screen, settings.COLOR["LIGHTGRAY"], (0, y), (settings.MAP_WIDTH, y))

    def draw(self):
        # Background
        self.screen.fill(settings.COLOR["BLACK"])
        # Tiles
        self.map.draw(self.screen)
        # Overlay
        self.draw_grid_overlay()
        # Flip
        pg.display.flip()

    def events(self):
        # catch events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                
