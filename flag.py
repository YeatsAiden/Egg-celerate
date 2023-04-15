import pygame
from consts import *


class Flag:
    def __init__(self, pos):
        self.pos = pos
        self.image = finish_img
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        self.collision = False

    
    def check_collision(self, rect):
        if self.rect.colliderect(rect):
            self.collision = True
        
        if self.collision:
            return True
        elif not self.collision:
            return False
    

    def draw(self, surf, scroll):
        surf.blit(self.image, [self.rect.x - scroll[0], self.rect.y - scroll[1]])
