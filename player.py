import pygame
import math
from consts import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        pygame.sprite.Sprite.__init__(self)
        # Players position.
        self.start_pos = list(pos)
        self.image = image
        # Player mass
        self.mass = 50
        # Player hit box.
        self.rect = pygame.Rect(self.start_pos[0], self.start_pos[1], self.image.get_width(), self.image.get_height())

        self.player_state = {
            "moving_right": False,
            "moving_left": False,
            "jumping": False
        }

        self.collision_state = {
            "right": False,
            "left": False,
            "top": False,
            "bottom": False
        }

        self.max_fall_speed = 10

        self.can_jump = False

        self.jump_force = 4

        self.wall_jump_force = (20, 5)

        self.wall_jump_cooldown = 0.5

        self.prev_wall_jump_time = 0

        self.speed = 0.5

        self.momentum = 0

        self.gravity = 0

        self.heading = pygame.Vector2(0, 0)

    def update(self, current_level_tiles, delta_time, current_time):  # this runs every frame
        self.move(current_level_tiles, delta_time, current_time)

    def move(self, tiles, delta_time, current_time):
        self.heading.x, self.heading.y = 0, 0

        # Movement
        if self.player_state['moving_right']:
            self.momentum += self.speed

        if self.player_state['moving_left']:
            self.momentum -= self.speed

        if not self.player_state['moving_left'] and not self.player_state['moving_right']:
            if -0.1 < self.momentum < 0.1:
                self.momentum = 0
            else:
                self.momentum /= 1.1

        self.momentum = max(min(self.momentum, 2), -2)


        if self.player_state['jumping'] and self.can_jump:
            jump_noise.play()
            self.can_jump = False
            self.gravity = 0
            self.gravity += -self.jump_force

        self.gravity += g * self.mass
        if self.gravity > self.max_fall_speed:
            self.gravity = self.max_fall_speed

        self.heading.x += self.momentum
        self.heading.y += self.gravity


        self.wall_jump_stuff(current_time)
        self.collision_check(tiles, delta_time)


    def collision_check(self, tiles, dt):
        self.collision_state = {"right": False, "left": False, "top": False, "bottom": False}

        self.rect.x += math.floor(self.heading.x) if self.heading.x > 0 else math.ceil(self.heading.x)

        for tile in tiles:
            if tile.colliderect(self.rect):
                if self.heading.x < 0:
                    self.collision_state['left'] = True
                    self.rect.left = tile.right
                    self.momentum = 0

                if self.heading.x > 0:
                    self.collision_state['right'] = True
                    self.rect.right = tile.left
                    self.momentum = 0

        self.rect.y += round(self.heading.y)

        for tile in tiles:
            if tile.colliderect(self.rect):
                if self.heading.y > 0:
                    self.rect.bottom = tile.top
                    self.collision_state['bottom'] = True
                    self.can_jump = True
                    self.gravity = 0

                if self.heading.y < 0:
                    self.rect.top = tile.bottom
                    self.collision_state['top'] = True
                    self.gravity = 0
    

    def wall_jump_stuff(self, current_time):
        can_wall_jump = (self.collision_state['right'] or self.collision_state['left']) and not self.collision_state['bottom']
        if can_wall_jump:
            self.gravity = 1 if self.heading.y > 0 else self.gravity
            if self.player_state['jumping'] and (current_time - self.prev_wall_jump_time > self.wall_jump_cooldown): 
                self.prev_wall_jump_time = current_time
                self.can_jump = True
                self.momentum = self.wall_jump_force[0] if self.collision_state['left'] else -self.wall_jump_force[0]
