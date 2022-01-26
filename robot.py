import pygame as pg

from size_constants import *

default_pos = (0.5,0.5)

class Robot(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.sprite = pg.image.load('robit.png').convert_alpha()
        self.rect = self.sprite.get_rect()
        self.rect.centerx = int(default_pos[0] * PIXELS_PER_TILE)
        self.rect.centery = int(default_pos[1] * PIXELS_PER_TILE)
        self.angle = 0
        self.update_sprite_angle()

    def erase(self, screen, arena):
        screen.blit(arena.image, (0,0))#area=self.angled_sprite.get_rect())

    def update_sprite_angle(self):
        self.angled_sprite = pg.transform.rotate(self.sprite,
                                        self.angle)
        self.angled_rect = self.angled_sprite.get_rect()
        self.angled_rect.center = self.rect.center

    def render(self, screen):
        screen.blit(self.angled_sprite, self.angled_rect)

