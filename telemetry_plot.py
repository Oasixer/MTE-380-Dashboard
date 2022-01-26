import pygame as pg

from size_constants import TLBR

Y_LABEL_WIDTH = 50
PLOT_BACKGROUND_COLOUR = (255,255,255) # where the actual data goes (inner)
Y_LABEL_BACKGROUND_COLOUR = PLOT_BACKGROUND_COLOUR
TITLE_PAD = 40
PAD = (TITLE_PAD, Y_LABEL_WIDTH, 0, 0)
BACKGROUND_COLOUR = (60,60,60)
TITLE_COLOUR = (0,0,0)
AXIS_LABEL_COLOUR = (25,25,25)
AXIS_LABEL_FONTSIZE = 15
DATA_POINT_SIZE = 1 # pixels of diameter/width per data point square/circle
PLOT_SIZE = (100,100) # pixels for the size of the inner plot
DISPLAY_DATA_POINTS = PLOT_SIZE[0] / DATA_POINT_SIZE
if DISPLAY_DATA_POINTS - int(DISPLAY_DATA_POINTS) != 0: # pixel ratio mismatch
    raise Exception

PLOT_MARGIN = (0 10 10 0)

class TelemetryPlot:
    def __init__(self, title, row, col):
        self.plot_size = PLOT_SIZE
        total_height = PAD[TLBR.T]+plot_size[0]+PAD[TLBR.B]
        total_width = PAD[TLBR.L]+plot_size[0]+PAD[TLBR.R]
        self.rect = pg.Rect(ROW*(PLOT_MARGIN[TLBR.T] + total_height + PLOT_MARGIN[TLBR.B]),ARENA_SIZE+COL*(PLOT_MARGIN[TLBR.L] + total_width + PLOT_MARGIN[TLBR.R]),
                     PAD[TLBR.L]+plot_size[0]+PAD[TLBR.R],
                     PAD[TLBR.T]+plot_size[1]+PAD[TLBR.B])
        self.title_font = pg.font.SysFont('Arial', 30)
        self.axis_label_font = pg.font.SysFont('Arial', AXIS_LABEL_FONTSIZE)
        self.plot_image = self.generate_plot_image()
        self.plot_image_rect = self.plot_image.get_rect()
        self.plot_image_rect.top = self.rect.top + self.PAD[TLBR.T]
        self.plot_image_rect.left = self.rect.left + self.PAD[TLBR.L]
        self.background_image = self.generate_background_image()
        self.y_label_area_image = self.generate_y_label_area_image()
        self.y_label_area_image_rect = self.y_label_area_image.get_rect()
        self.y_label_area_image_rect.left = self.rect.left
        self.y_label_area_image_rect.top = self.rect.top + self.PAD[TLBR.T]
        self.values = collections.Deque([],maxlen=DISPLAY_DATA_POINTS)
        self.new_value = None

    def update_value(self, new_value):
        self.new_value = new_value

    def render_init(self, screen):
        screen.blit(self.background_image, self.rect)
        screen.blit(self.y_label_area_image, self.y_label_area_image_rect)
        screen.blit(self.plot_image, self.plot_image_rect)

    #  def render(self, screen):
        #  for val in self.values:
        # TODO PIXEL MATH
            #  screen.set_at(())
        #  self.values.append()

    def generate_y_label_area_image(self):
        image = pg.Surface(Y_LABEL_WIDTH,self.plot_size[1])
        image.fill(PLOT_BACKGROUND_COLOUR)
        return image

    def generate_plot_image(self):
        image = pg.Surface(self.plot_size)
        image.fill(PLOT_BACKGROUND_COLOUR)
        return image

    def generate_background_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(BACKGROUND_COLOUR)
        title_surf = self.title_font.render(self.title, False, TITLE_COLOUR)
        image.blit(title_surf,(0,5))

class TelemetryPlots:
    def __init__(self):
        self.plots = [[TelemetryPlot()]]
