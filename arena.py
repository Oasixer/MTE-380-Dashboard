import pygame as pg

from size_constants import *
from tile import Tile

class Arena(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(0,0,ARENA_SIZE_PIXELS,ARENA_SIZE_PIXELS)
        self.tiles = self.generate_tiles()
        self.segments = self.generate_segments()
        
        self.image = self.generate_image()


    def generate_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill((0,255,0))
        rect = image.get_rect()
        for row in range(6):
            for col in range(6):
                if row % 2 == col % 2:
                    pg.draw.rect(image, (255,0,0), pg.Rect(col* PIXELS_PER_TILE, row * PIXELS_PER_TILE, PIXELS_PER_TILE, PIXELS_PER_TILE))

        for segment in self.segments:
            segment.render(image)

        return image

    def generate_tiles(self):
        tiles = []
        for row in range(6):
            new_row = []
            for col in range(6):
                new_row.append(Tile(row, col))
            tiles.append(new_row)
        return tiles

    def generate_segments(self):
        segments = [
            Line(start=(3.5,5.5), end=(1,5.5)),
            Line(start=(0.5,5), end=(0.5,1)),
            Line(start=(1,0.5), end=(5,0.5)),
            Line(start=(5.5,1), end=(5.5,4)),
            Line(start=(5,4.5), end=(2,4.5)),
            Line(start=(1.5,4), end=(1.5,2)),
            Line(start=(2,1.5), end=(4,1.5)),
            Line(start=(4.5,2), end=(4.5,3)),
            Line(start=(4,3.5), end=(3,3.5))
        ]
        return segments

class Segment:
    def __init__(self, activated=False):
        self.activated = activated

    def distance(self, point):
        raise NotImplementedError

    def render(self, surface):
        raise NotImplementedError

LINE_COLOUR = (150,150,150)

class Line(Segment):
    def __init__(self, start, end):
        self.start = [i*PIXELS_PER_TILE for i in start]
        self.end = [i*PIXELS_PER_TILE for i in end]

    def render(self, surface):
        pg.draw.line(surface, LINE_COLOUR, self.start, self.end, 3)

    def distance(self, point):
        # im gonna just be lazy as shit and rely on the fact that the lines
        # are currently guaranteed to be horizontal or vertical to skip the grade 10 calculus
        # of calculating distance to an arbitrary line between (start) and (end)
        if self.start[0] == self.end[0]:
            # vertical line, distance is just x value
            return point[0]-start[0]
        elif self.start[1] == self.end[1]:
            # horizontal line, distance is y value
            return point[1]-start[1]
