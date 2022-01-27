import pygame as pg
import os
import sys
import random
import numpy as np

from robot import Robot
from arena import Arena
from telemetry_plot import TelemetryPlots

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
        #  self.textsurface_1 = self.font.render('telemetry graphs go here', False, (255, 255, 255))
        self.screen.blit(self.arena.image, (0,0))
        self.telemetry_plots = TelemetryPlots()
        self.telemetry_plots.render_init(self.screen)
        #  self.telemetry_plots = TelemetryPlots()

        self.fake_y_vel = 3 # fake data for plot testing
        self.fake_x_vel = 3

    def update_robot_data(self):
        if FAKE:

            clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
            self.fake_y_vel = clamp(self.fake_y_vel+np.random.normal(scale=1)/10, -5, 5)
            self.fake_x_vel = clamp(self.fake_x_vel+np.random.normal(scale=1)/100, -5, 5)
            if self.robot.rect.centery > 5*PIXELS_PER_TILE and self.fake_y_vel > 0:
                self.fake_y_vel -= 0.1*max(abs(self.fake_y_vel),1) if self.robot.rect.bottom-self.arena.rect.bottom>3 else 5
            elif self.robot.rect.centery < 1*PIXELS_PER_TILE and self.fake_y_vel < 0:
                self.fake_y_vel += 0.1*max(abs(self.fake_y_vel),1) if self.robot.rect.top>3 else 5
            self.fake_x_vel += np.random.normal(scale=5)/10
            if self.robot.rect.centerx > 5*PIXELS_PER_TILE and self.fake_x_vel > 0:
                self.fake_x_vel -= 0.1*max(abs(self.fake_x_vel),1) if self.robot.rect.right-self.arena.rect.right>3 else 20
            elif self.robot.rect.centerx < 1*PIXELS_PER_TILE and self.fake_x_vel < 0:
                self.fake_x_vel += 0.1*max(abs(self.fake_x_vel),1) if self.robot.rect.left>3 else 10

            self.robot.angle = np.degrees(np.tan(self.fake_x_vel/self.fake_y_vel))%360
            #  print(f'self.robot_angle: {self.robot.angle}')
            #  print(f'self.fake_x_vel: {self.fake_x_vel}')
            #  print(f'self.fake_y_vel: {self.fake_y_vel}')
            self.robot.update_sprite_angle() 

            fake_y_vel_pixels = self.fake_y_vel * PIXELS_PER_TILE * SPF
            fake_x_vel_pixels = self.fake_x_vel * PIXELS_PER_TILE * SPF
            self.robot.rect.move_ip(fake_x_vel_pixels,fake_y_vel_pixels)
            #  print(f'fake_x_vel_pixels: {fake_x_vel_pixels}')
            #  print(f'fake_y_vel_pixels: {fake_y_vel_pixels}')
            self.telemetry_plots.y_vel.update_value(self.fake_y_vel)
            self.telemetry_plots.x_vel.update_value(self.fake_x_vel)

            self.telemetry_plots.robot_angle.update_value(self.robot.angle)

    def render_plots(self):
        self.telemetry_plots.render(self.screen)

    def erase(self):
        # eventually erase previous telemetry data here
        self.robot.erase(self.screen, self.arena)

    def render(self):
        self.robot.render(self.screen)
        #  self.screen.blit(self.textsurface_1,(900,100))
        self.render_plots()
        pg.display.update()

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                sys.exit()
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
