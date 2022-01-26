import pygame as pg

from size_constants import *
from tile import Tile

class Arena(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.rect = pg.Rect(0,0,ARENA_SIZE_PIXELS,ARENA_SIZE_PIXELS)
        self.tiles = self.generate_tiles()
        self.image = self.generate_image()


    def generate_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill((0,255,0))
        rect = image.get_rect()
        for row in range(6):
            for col in range(6):
                if row % 2 == col % 2:
                    pg.draw.rect(image, (255,0,0), pg.Rect(col* PIXELS_PER_TILE, row * PIXELS_PER_TILE, PIXELS_PER_TILE, PIXELS_PER_TILE))
        return image


    def generate_tiles(self):
        tiles = []
        for row in range(6):
            new_row = []
            for col in range(6):
                new_row.append(Tile(row, col))
            tiles.append(new_row)
        return tiles

