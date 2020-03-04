import sys
import pygame as pg

import game_settings as settings
import game_map as gamemap

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

        if keystate[pg.K_w]:
            self.map.camera.move(dy=-1)
        if keystate[pg.K_s]:
            self.map.camera.move(dy=1)
        if keystate[pg.K_a]:
            self.map.camera.move(dx=-1)
        if keystate[pg.K_d]:
            self.map.camera.move(dx=1)

    def draw_grid_overlay(self):
        for x in range(0, settings.MAP_WIDTH, settings.TILE_SIZE):
            pg.draw.line(self.screen, settings.COLOR["LIGHTGRAY"], (x, 0), (x, settings.MAP_HEIGHT))
        for y in range(0, settings.MAP_HEIGHT, settings.TILE_SIZE):
            pg.draw.line(self.screen, settings.COLOR["LIGHTGRAY"], (0, y), (settings.MAP_WIDTH, y))

    def draw(self):
        # Background
        self.screen.fill(settings.COLOR["WHITE"])
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
