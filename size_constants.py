from enum import Enum

SCREEN_SIZE = (1700,900)
ARENA_SIZE_INCHES = 72
PIXELS_PER_INCH = 10
INCHES_PER_TILE = 12
PIXELS_PER_TILE = INCHES_PER_TILE * PIXELS_PER_INCH
ARENA_SIZE_PIXELS = PIXELS_PER_INCH * ARENA_SIZE_INCHES

class TRBL(Enum): # helper because I never learned how to count
    T = 0 # top
    R = 1 # right
    B = 2 # bottom
    L = 3 # left (just like CSS)
