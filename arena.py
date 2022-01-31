import pygame as pg
import functools
import math

from size_constants import *
from tile import Tile

TILE_COLOUR_1 = (60,60,60)
TILE_COLOUR_2 = (30,100,100)

HEADING_ERROR_ARC_COLOUR = (100,200,255)

LINE_COLOUR = (150,150,150)
LINE_COLOUR2 = (150,150,0)
NEAREST_DIST_LINE_COLOUR = (255,255,0)
LINE_THICK=3

class Arena():
    def __init__(self, robot):
        self.rect = pg.Rect(0,0,ARENA_SIZE_PIXELS,ARENA_SIZE_PIXELS)
        self.robot = robot
        self.tiles = self.generate_tiles()
        self.segments = self.generate_segments()
        
        self.image = self.generate_image()

    def erase(self, screen):
        screen.blit(self.image, (0,0))


    def generate_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TILE_COLOUR_1)
        rect = image.get_rect()
        for row in range(6):
            for col in range(6):
                if row % 2 == col % 2:
                    pg.draw.rect(image, TILE_COLOUR_2, pg.Rect(col* PIXELS_PER_TILE, row * PIXELS_PER_TILE, PIXELS_PER_TILE, PIXELS_PER_TILE))

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
            CornerCircle(center=(1,5),corner=Diagonal.BL),
            Line(start=(0.5,5), end=(0.5,1)),
            CornerCircle(center=(1,1),corner=Diagonal.TL),
            Line(start=(1,0.5), end=(5,0.5)),
            CornerCircle(center=(5,1),corner=Diagonal.TR),
            Line(start=(5.5,1), end=(5.5,4)),
            CornerCircle(center=(5,4),corner=Diagonal.BR),
            Line(start=(5,4.5), end=(2,4.5)),
            CornerCircle(center=(2,4),corner=Diagonal.BL),
            Line(start=(1.5,4), end=(1.5,2)),
            CornerCircle(center=(2,2),corner=Diagonal.TL),
            Line(start=(2,1.5), end=(4,1.5)),
            CornerCircle(center=(4,2),corner=Diagonal.TR),
            Line(start=(4.5,2), end=(4.5,3)),
            CornerCircle(center=(4,3),corner=Diagonal.BR),
            Line(start=(4,3.5), end=(3,3.5)),
            CornerCircle(center=(3,3),corner=Diagonal.BL),
            CornerCircle(center=(3,3),corner=Diagonal.TL),
            CornerCircle(center=(1,1),corner=Diagonal.TL)
        ]
        return segments

class Segment:
    def __init__(self, activated=False):
        self.activated = activated

    def distance(self, point):
        raise NotImplementedError

    def render(self, surface):
        raise NotImplementedError


class CornerCircle(Segment):
    def __init__(self, center, corner):
        super().__init__(self)
        self.circle_center = [i*PIXELS_PER_TILE for i in center]
        self.corner = corner
        self.radius_tiles = 0.5
        self.radius_pixels = int(self.radius_tiles*PIXELS_PER_TILE)
        self.image = self.generate_image()
        self.rect = self.image.get_rect()
        if self.corner is Diagonal.TR:
            center_offset = (self.rect.width/2, -self.rect.height/2)
        elif self.corner is Diagonal.BL:
            center_offset = (-self.rect.width/2, self.rect.height/2)
        elif self.corner is Diagonal.TL:
            center_offset = (-self.rect.width/2, -self.rect.height/2)
        else:
            center_offset = (self.rect.width/2, self.rect.height/2)

        self.rect.center = (self.circle_center[0]+center_offset[0],self.circle_center[1]+center_offset[1])

    def distance(self, pos): # position in pixels

        # returns negative if inside circle, positive if outside circle
        return ((pos[0]-self.circle_center[0])**2+(pos[1]-self.circle_center[1])**2)**0.5 - self.radius_pixels

    def get_nearest(self, pos): # get nearest point on the circle
        #  dist = self.distance(pos) # distance to the curve
        #  print(f'dist: {dist}')
        #  center_dist = ((pos[0]-self.circle_center[0])**2+(pos[1]-self.circle_center[1])**2)**0.5 # dist to center of circle
        #  #  print(center_dist)

        #  x_dist_from_center = (abs(dist)/center_dist)*(pos[0]-self.circle_center[0])
        #  y_dist_from_center = (abs(dist)/center_dist)*(pos[1]-self.circle_center[1])
        #  print(f'x_dist: {x_dist_from_center}, y_dist: {y_dist_from_center}')
        #  nearest = (self.circle_center[0]-x_dist_from_center, self.circle_center[1]-y_dist_from_center)
        #  print(f'nearest: {nearest}')
        x1 = pos[0]
        y1 = pos[1]

        xc = self.circle_center[0]
        yc = self.circle_center[1]

        R = self.radius_pixels
        # dist from robot to center of circle
        r = ((pos[0]-self.circle_center[0])**2+(pos[1]-self.circle_center[1])**2)**0.5
        sign = functools.partial(math.copysign, 1)
        x_sign = sign(x1-xc)
        y_sign = -sign(y1-yc)
        
        #  x2 = ((x1 - xc)/r)*R+xc
        #  y2 = ((y1 - yc)/r)*R+yc
        x2 = (-x_sign*(x1-xc)/r)*R+xc
        y2 = (-y_sign*(y1-yc)/r)*R+yc
        return (x2,y2)

    def generate_image(self):
        image = pg.Surface((self.radius_pixels, self.radius_pixels)).convert_alpha()
        image.fill((0,0,0,0))
        rect = image.get_rect()
        if self.corner is Diagonal.TR:
            center = rect.bottomleft
        elif self.corner is Diagonal.TL:
            center = rect.bottomright
        elif self.corner is Diagonal.BL:
            center = rect.topright
        else:
            center = rect.topleft

        pg.draw.circle(image, LINE_COLOUR2, center, self.radius_pixels, 3)
        return image

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def generate_perp_line(self, robot):
        pos = robot.rect.center
        nearest = self.get_nearest(pos)
        nearest_line_width = abs(nearest[0]-self.circle_center[0])
        nearest_line_height = abs(nearest[1]-self.circle_center[1])
        
        #  image = pg.Surface((nearest_line_width,nearest_line_height)).convert_alpha()
        image = pg.Surface((ARENA_SIZE_PIXELS, ARENA_SIZE_PIXELS)).convert_alpha()

        image.fill((0,0,0,0))
        pg.draw.line(image, NEAREST_DIST_LINE_COLOUR, pos, nearest, LINE_THICK)

        desired_heading_arc_rect = pg.Rect(0,0,40,40)
        desired_heading_arc_rect.center = pos
        angle_of_desired_heading = angle_between_positions(pos,nearest)
        robot.angle_error = (angle_of_desired_heading-robot.angle)%360
        heading_angle_pg = angle_to_pg_angle(angle_of_desired_heading)
        robot_angle_pg = angle_to_pg_angle(robot.angle)
        start_angle = min(heading_angle_pg, robot_angle_pg)
        end_angle = max(heading_angle_pg, robot_angle_pg)
        desired_heading_arc_rect.center = pos
        pg.draw.arc(image,HEADING_ERROR_ARC_COLOUR,desired_heading_arc_rect,start_angle,end_angle,3)
        return image


class Line(Segment):
    def __init__(self, start, end):
        self.start = [i*PIXELS_PER_TILE for i in start]
        self.end = [i*PIXELS_PER_TILE for i in end]
        self.horizontal = self.start[0] == self.end[0]

    def render(self, surface):
        pg.draw.line(surface, LINE_COLOUR, self.start, self.end, LINE_THICK)

    def distance(self, point):
        # im gonna just be lazy as shit and rely on the fact that the lines
        # are currently guaranteed to be horizontal or vertical to skip the grade 10 calculus
        # of calculating distance to an arbitrary line between (start) and (end)
        if self.horizontal:
            # vertical line, distance is just x value
            return point[0]-start[0]
        else:
            # horizontal line, distance is y value
            return point[1]-start[1]

    #  def nearest(self, point):
        #  if 
