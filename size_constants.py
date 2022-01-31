from enum import Enum

SCREEN_SIZE = (1700,900)
ARENA_SIZE_INCHES = 72
PIXELS_PER_INCH = 10
INCHES_PER_TILE = 12
PIXELS_PER_TILE = INCHES_PER_TILE * PIXELS_PER_INCH
print(f'PIXELS_PER_TILE: {PIXELS_PER_TILE}')
ARENA_SIZE_PIXELS = PIXELS_PER_INCH * ARENA_SIZE_INCHES

def pixels_to_tiles(pixel_loc):
    return (pixel_loc[0]/PIXELS_PER_TILE, pixel_loc[1]/PIXELS_PER_TILE)

def tiles_to_pixels(tile_loc):
    return (tile_loc[0]*PIXELS_PER_TILE, tile_loc[1]*PIXELS_PER_TILE)

class TRBL(Enum): # helper because I never learned how to count
    T = 0 # top
    R = 1 # right
    B = 2 # bottom
    L = 3 # left (just like CSS)

class Diagonal(Enum): # for corner circles
    TL = 0 # top left
    TR = 1 # top right
    BL = 2 # bottom left
    BR = 3 # bottom right
