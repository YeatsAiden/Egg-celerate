import pygame
import math
from consts import *


class Egg(pygame.sprite.Sprite):
    def __init__(self, player_pos, mouse_pos, image, scroll):
        pygame.sprite.Sprite.__init__(self)
        self.egg_pos = player_pos
        
        self.egg_image = image
        self.image = image

        self.rect = pygame.Rect(self.egg_pos[0], self.egg_pos[1], self.egg_image.get_width(), self.egg_image.get_height())

        self.throw_force = 4
        self.max_speed = 7
        self.min_speed = 1

        self.x_change = mouse_pos[0] - player_pos[0] 
        self.y_change = mouse_pos[1] - player_pos[1] + scroll[1]

        self.angle = math.degrees(math.atan2(-self.y_change, self.x_change))

        self.draw_angle = self.angle

        self.heading = pygame.Vector2(0, 0)
        self.gravity = 0
        self.max_fall_speed = 10
        self.mass = 40

        self.collided = False
        self.collision_pos = self.rect.topleft
        self.exploded = False

    
    def update(self, current_level_tiles, delta_time, current_time):
        self.fly(current_level_tiles)

    
    def fly(self, tiles):
        self.heading.x, self.heading.y = 0, 0
        self.image = pygame.transform.rotate(self.egg_image, self.draw_angle - 45)

        self.gravity += g * self.mass

        self.heading.x += math.cos(math.radians(self.angle)) * self.throw_force
        self.heading.y += math.sin(math.radians(-self.angle)) * self.throw_force + self.gravity

        self.draw_angle = math.degrees(math.atan(self.heading.x/self.heading.y)) - 45

        self.collision_check(tiles)
        self.wrap_egg()
    

    def collision_check(self, tiles):
        self.rect.x += round(self.heading.x)
        self.rect.y += round(self.heading.y)
        for tile in tiles:
            if tile.colliderect(self.rect):
                if not self.collided:
                    self.collision_pos = [self.rect.x + int(self.egg_image.get_width()/2), self.rect.y + int(self.egg_image.get_height()/2)]
                self.egg_image = transparent_egg_img
                self.collided = True
    

    def explode(self, player_pos):
        self.x_ex_change = player_pos[0] - self.collision_pos[0] 
        self.y_ex_change = player_pos[1] - self.collision_pos[1]
        self.explode_angle = math.degrees(math.atan2(-self.y_change, self.x_change))
        distance = math.sqrt(self.x_ex_change**2 + self.y_ex_change**2)
        if distance <= 50:
            return True, self.explode_angle
        else:
            return False, 0
    
    def wrap_egg(self):
        if self.rect.x <= -self.rect.width:
            self.rect.x = display_size[0] - 3
        elif self.rect.x >= display_size[0]:
            self.rect.x = -self.rect.width + 3


