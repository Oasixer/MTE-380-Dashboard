import pygame as pg
from collections import deque

from size_constants import *

Y_LABEL_WIDTH = 50
PLOT_BACKGROUND_COLOUR = (255,255,255) # where the actual data goes (inner)
DATA_POINT_COLOUR = (200,0,200) # where the actual data goes (inner)
Y_LABEL_BACKGROUND_COLOUR = PLOT_BACKGROUND_COLOUR
TITLE_PAD = 40
PAD = (TITLE_PAD, Y_LABEL_WIDTH, 0, 0)
BACKGROUND_COLOUR = (60,60,60)
TITLE_COLOUR = (0,0,0)
AXIS_LABEL_COLOUR = (25,25,25)
AXIS_LABEL_FONTSIZE = 15
DATA_POINT_SIZE = 1 # pixels of diameter/width per data point square/circle
PLOT_SIZE = (100,100) # pixels for the size of the inner plot
DISPLAY_DATA_POINTS = PLOT_SIZE[0]
DATA_POINT_SIZE = 1

PLOT_MARGIN = (0, 10, 10, 0)

class TelemetryPlot:
    def __init__(self, title, row, col, tick_increment):
        self.title = title
        self.tick_increment = tick_increment
        self.plot_size = PLOT_SIZE
        total_height = PAD[TLBR.T.value]+self.plot_size[0]+PAD[TLBR.B.value]
        total_width = PAD[TLBR.L.value]+self.plot_size[0]+PAD[TLBR.R.value]
        self.rect = pg.Rect(row*(PLOT_MARGIN[TLBR.T.value] + total_height + PLOT_MARGIN[TLBR.B.value]),ARENA_SIZE_PIXELS+col*(PLOT_MARGIN[TLBR.L.value] + total_width + PLOT_MARGIN[TLBR.R.value]),
                     PAD[TLBR.L.value]+self.plot_size[0]+PAD[TLBR.R.value],
                     PAD[TLBR.T.value]+self.plot_size[1]+PAD[TLBR.B.value])
        self.title_font = pg.font.SysFont('Arial', 30)
        self.axis_label_font = pg.font.SysFont('Arial', AXIS_LABEL_FONTSIZE)
        self.plot_image = self.generate_plot_image()
        self.plot_image_rect = self.plot_image.get_rect()
        self.plot_image_rect.top = self.rect.top + PAD[TLBR.T.value]
        self.plot_image_rect.left = self.rect.left + PAD[TLBR.L.value]
        self.background_image = self.generate_background_image()
        self.y_label_area_image = self.generate_y_label_area_image()
        self.y_label_area_image_rect = self.y_label_area_image.get_rect()
        self.y_label_area_image_rect.left = self.rect.left
        self.y_label_area_image_rect.top = self.rect.top + PAD[TLBR.T.value]
        self.values = deque([1,2],maxlen=DISPLAY_DATA_POINTS)
        self.scale_factor = 1
        self.display_scale_min = min(self.values)
        self.display_scale_min = max(self.values)
        self.display_scale_pad = 0.1 # 10%
        self.pixel_scale_factor = None
        self.new_value = None
        self.ticks = {}

    def update_value(self, new_value):
        self.new_value = new_value

    def render_init(self, screen):
        screen.blit(self.background_image, self.rect)
        screen.blit(self.y_label_area_image, self.y_label_area_image_rect)
        screen.blit(self.plot_image, self.plot_image_rect)

    def erase_update_render(self, screen):
        if self.pixel_scale_factor is not None:
            for i in range(len(self.values)):
                screen.set_at((self.rect.right-i,int(self.rect.bottom+(self.values[-i]-self.display_scale_min)/self.pixel_scale_factor)), (PLOT_BACKGROUND_COLOUR))

        self.values.append(self.new_value)
        
        new_min = min(self.values)
        new_max = max(self.values)

        if new_min != self.display_scale_min or new_max != self.display_scale_max:
            breadth = new_max-new_min
            new_fullscale = new_max - new_min+breadth*2*self.display_scale_pad
            new_pixel_scale_factor = self.plot_size[1]/new_fullscale

            first_tick = (int(new_min / self.tick_increment)-1)*self.tick_increment
            first_tick = first_tick if first_tick > new_min-self.display_scale_pad*(new_max-new_min) else (int(new_min / self.tick_increment))*self.tick_increment

            last_tick = (int(new_max / self.tick_increment))*self.tick_increment
            last_tick = last_tick if last_tick > new_max+self.display_scale_pad*(new_max-new_min) else (int(new_max / self.tick_increment)-1)*self.tick_increment

            new_tick = first_tick
            new_ticks = {}
            screen.blit(self.y_label_area_image, self.y_label_area_image_rect)
            while(new_tick) <= last_tick:
                try:
                    new_ticks[new_tick] = self.ticks[new_tick]
                except KeyError:
                    new_ticks[new_tick] = self.generate_tick(new_tick)

                #  print('blitting')
                screen.blit(new_ticks[new_tick], (self.rect.left,self.rect.bottom + (new_tick-new_min)/ new_pixel_scale_factor))
                new_tick += self.tick_increment

            self.ticks = new_ticks
            self.pixel_scale_factor = new_pixel_scale_factor
        self.display_scale_max = new_max
        self.display_scale_min = new_min

        for i in range(len(self.values)):
            screen.set_at((self.rect.right-i,self.rect.bottom+int((self.values[-i]-self.display_scale_min)/self.pixel_scale_factor)),DATA_POINT_COLOUR)

# (200,0,200)
        #  self.values.append()
    def generate_tick(self,val):
        height = 15
        image = pg.Surface((50,height)).convert_alpha()
        image.fill(BACKGROUND_COLOUR)
        tick_label_surf = self.axis_label_font.render(str(val), False, TITLE_COLOUR)
        image.blit(tick_label_surf, (0, height/2 - tick_label_surf.get_rect().height/2))
        return image

    def generate_y_label_area_image(self):
        image = pg.Surface((Y_LABEL_WIDTH,self.plot_size[1])).convert_alpha()
        image.fill(PLOT_BACKGROUND_COLOUR)
        return image

    def generate_plot_image(self):
        image = pg.Surface((self.plot_size[0], self.plot_size[1])).convert_alpha()
        image.fill(PLOT_BACKGROUND_COLOUR)
        return image

    def generate_background_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(BACKGROUND_COLOUR)
        title_surf = self.title_font.render(self.title, False, TITLE_COLOUR)
        image.blit(title_surf,(0,5))
        return image

class TelemetryPlots:
    def __init__(self):
        self.y_vel_plot = TelemetryPlot('y_vel',0,0,0.1)
        self.plots = [[self.y_vel_plot]]

    def render_init(self, screen):
        for row in self.plots:
            for plot in row:
                plot.render_init(screen)

    def render(self, screen):
        for row in self.plots:
            for plot in row:
                plot.erase_update_render(screen)
