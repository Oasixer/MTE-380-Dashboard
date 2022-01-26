import pygame as pg
import os
import sys

from robot import Robot
from arena import Arena

from size_constants import *

# 720 x 720 @ 10 PIXELS_PER_INCH
FPS = 30
SPF = 1/FPS
FAKE = True

CAPTION = "yo momma"

class App:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.screen = pg.display.get_surface()
        self.robot = Robot()
        self.keys = pg.key.get_pressed()
        pg.font.init()
        self.font = pg.font.SysFont('Arial', 30)
        self.arena = Arena()
        self.textsurface_1 = self.font.render('telemetry graphs go here', False, (255, 255, 255))
        self.screen.blit(self.arena.image, (0,0))

        #  self.telemetry_plots = TelemetryPlots()

    def update_robot_data(self):
        if FAKE:
            x_spd_temp = 3

            self.robot.rect.move_ip(0,x_spd_temp)
            self.robot.angle += 2
            self.robot.update_sprite_angle() 

            self.robot.velocity_x = (x_spd_temp/PIXELS_PER_TILE) / SPF

    def erase(self):
        # eventually erase previous telemetry data here
        self.robot.erase(self.screen, self.arena)

    def render(self):
        self.robot.render(self.screen)
        self.screen.blit(self.textsurface_1,(900,100))
        pg.display.update()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def main_loop(self):
        while(True):
            self.clock.tick(FPS)
            self.event_loop()
            self.erase()
            self.update_robot_data()
            self.render()

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    App().main_loop()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
