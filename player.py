import pygame
import math
from consts import *
import egg


class Player():
    def __init__(self, pos, image):
        # Players position.
        self.pos = pos
        #Player's image
        self.image = image
        # Player mass
        self.mass = 50
        # Player hit box.
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        self.player_state = {
            "moving_right": False,
            "moving_left": False,
            "jumping": False,
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
        self.velocity = [0, 0]
        self.gravity = 0
        self.heading = pygame.Vector2(0, 0)
        self.count = 0
        self.throw_cooldown = 0.5
        self.prev_throw_time = 0

        self.vel_array = []

        self.height = 0


    def update(self, current_level_tiles, delta_time, current_time):  
        self.move(current_level_tiles, delta_time, current_time)
        self.wrap_player()
        self.timer()

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

        self.gravity += g * self.mass - self.velocity[1]
        if self.gravity > self.max_fall_speed:
            self.gravity = self.max_fall_speed
        
        for vel in self.vel_array:
            self.heading.x -= vel[0]
            self.heading.y -= vel[1]

            if -0.1 < vel[0] < 0.1:
                vel[0] = 0
            else:
                vel[0] /= 1.5

            if -0.1 < vel[1] < 0.1:
                vel[1] = 0
            else:
                vel[1] /= 1.5
            if vel[0] == 0 and vel[1] == 0:
                self.vel_array.remove(vel)
    
        self.heading.x += self.momentum - self.velocity[0]
        self.heading.y += self.gravity
        self.height = self.calc_height()

        self.wall_jump_stuff(current_time)
        self.collision_check(tiles)


    def collision_check(self, tiles):
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
    

    def throw_egg(self, mouse_pos, current_time, scroll):
        return egg.Egg([self.rect.x, self.rect.y], mouse_pos, egg_img, scroll)
    

    def timer(self):
        if self.collision_state['bottom']:
            self.count = 0
        else:
            self.count += 1
    

    def launch(self, angle):
        if angle[0]:
            velocity = [0, 0]
            velocity[0] += math.cos(math.radians(angle[1])) * 10
            velocity[1] += math.sin(math.radians(-angle[1])) * 10
            self.vel_array.append(velocity)


    def wrap_player(self):
        if self.rect.x <= -self.rect.width:
            self.rect.x = display_size[0] - 3
        elif self.rect.x >= display_size[0]:
            self.rect.x = -self.rect.width + 3


    def calc_height(self):
        return 3908 - self.rect.y