import sys
import pygame.sprite
from consts import *
import button
import time
import text
import player
import load_map
import animation
import particle
import random
import math


class Menu:
    def __init__(self, display, window):
        self.display = display
        self.window = window

        self.font = text.Font('assets/fonts/font.png', 0.5)

        self.animation = animation.Animation()

        self.player_img = pygame.image.load("assets/sprites/Player/idle/idle_0.png")
        self.player = player.Player((0, 0), self.player_img)
        self.player_frame = 0
        self.player_action = "idle"
        self.flip = False

        self.trail = particle.Particle(1)

        self.cursor_img = cursor_img
        self.mouse_pos = pygame.mouse.get_pos()

        self.map_loader = load_map.Load_map()

        self.Start = button.Button(10, 5, button_img, self.font, "Start")
        self.exit_button = button.Button(10, 25, button_img, self.font, "Exit")
        self.Menu = button.Button(180, 10, button_img, self.font, "Menu")

        self.all_sprites = []

        self.level_tiles = {
            "Level_one_tiles": self.map_loader.level_one_tiles
        }

        self.level_data = {
            "Level_one_data": self.map_loader.level_one_data
        }

        self.current_level = [self.level_data["Level_one_data"], self.level_tiles["Level_one_tiles"]]

        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.delta_time = 0

        self.scale = 1
        self.change = [0, 0]

        self.current_time = time.time()
        self.previous_time = time.time()

        self.eggs = []

        self.scroll = [0, 0]
        self.tile_scroll = [0, 0]

        self.in_game = False

        self.timer = 0
        self.hours = 0
        self.min = 2
        self.sec = 30
        self.total_sec = self.hours * 3600 + self.min * 60 + self.sec

        self.count_down_event = pygame.event.custom_type()
        pygame.time.set_timer(self.count_down_event, 1000)

        self.screen_shake = 0
        self.win = False
    

    def menu(func):
        def inside(self):
            is_running = True
            while is_running:
                self.display.fill((255, 249, 181))

                self.mouse_pos = pygame.mouse.get_pos()

                is_running = func(self)

                self.display.blit(self.cursor_img, (self.mouse_pos[0] / self.scale - 4, self.mouse_pos[1] / self.scale - 4))

                self.rescale_window()

                pygame.display.update()

                is_running = self.event_loop()

                self.clock.tick(60)
                
        return inside


    def game(self):
        self.win = False
        is_running = True
        self.in_game = True
        self.reset_timer()
        self.current_level = [self.level_data["Level_one_data"], self.level_tiles["Level_one_tiles"]]
        self.all_sprites.clear()
        self.player = player.Player((110, 3800), self.player_img)
        self.all_sprites.append([self.player, 0])
        while is_running:
            self.display.fill((163, 178, 210))

            self.mouse_pos = pygame.mouse.get_pos()

            self.current_time = time.time()
            self.previous_time = self.current_time

            if self.screen_shake > 0:
                self.screen_shake -= 1
            
            if self.screen_shake:
                self.scroll[0] += random.randint(0, 10) - 5
                self.scroll[1] += random.randint(0, 10) - 5

            self.scroll[0] = 0
            self.scroll[1] += (self.player.rect.y - self.scroll[1] - display_size[1]/2)/20
            self.tile_scroll = [int(self.scroll[0]), int(self.scroll[1])+2]

            self.decide_animation()
            self.animate()

            self.display.blit(bg_game_img, (0, 0))
            self.map_loader.draw_level(self.current_level[0], self.display, self.tile_scroll)
            self.draw_sprites(self.scroll, self.all_sprites)
            self.draw_sprites(self.scroll, self.eggs)
            self.trail.trail(self.display, self.player.rect.topleft, 10, self.scroll)
            self.particles(self.scroll)
            self.font.render(self.display, f'Height: {self.player.height}', 180, 10)
            self.font.render(self.display, f'Time: {self.timer}', 180, 20)
            self.display.blit(self.cursor_img, (self.mouse_pos[0] / self.scale - 4, self.mouse_pos[1] / self.scale - 4))

            self.update_sprites(self.current_level[1], self.delta_time, self.current_time, self.all_sprites)
            self.update_sprites(self.current_level[1], self.delta_time, self.current_time, self.eggs)

            self.rescale_window()

            pygame.display.update()

            is_running = self.event_loop()
            self.can_launch = False

            self.clock.tick(60)
            

    @menu
    def main_menu(self):
            self.in_game = False
            self.display.blit(bg_img, (0, 0))
            self.font.render(self.display, "Main Menu", 155, 10)

            if self.Start.draw(self.scale, self.change, self.display):
                time.sleep(0.2)
                self.game()

            if self.exit_button.draw(self.scale, self.change, self.display):
                time.sleep(0.2)
                pygame.quit()
                sys.exit()
            
            return True
                
    
    def rescale_window(self):
        # checks how the display should scale depending on the window size.
        self.scale = min(self.window.get_width() / self.display.get_width(), self.window.get_height() / self.display.get_height())

        # changes display size to new size using scale variable.
        surf = pygame.transform.scale(self.display, (self.scale * self.display.get_width(), self.scale * self.display.get_height()))

        self.change = [round((self.window.get_width() - surf.get_width()) / 2), round((self.window.get_height() - surf.get_height()) / 2)]

        # Keeps display surface in the center of the window.
        self.window.blit(surf, (self.change[0], self.change[1]))
    

    def event_loop(self):
        can_run = True
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_noise.play()
                time.sleep(0.2)
                pygame.quit()
                sys.exit()

            if self.in_game:
                if event.type == self.count_down_event:
                    can_run = self.countdown()
            
            if event.type == pygame.KEYDOWN:
                if self.in_game:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.player_state['moving_right'] = True
                        
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.player_state['moving_left'] = True

                    if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        self.player.player_state['jumping'] = True

                if event.key == pygame.K_ESCAPE:
                    click_noise.play()
                    time.sleep(0.2)
                    can_run, self.win = False , True

            if self.in_game:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0] and self.current_time - self.player.prev_throw_time > self.player.throw_cooldown:
                        self.player.prev_throw_time = self.current_time
                        mouse_pos = [self.mouse_pos[0] / self.scale + self.change[0] - 4, self.mouse_pos[1] / self.scale + self.change[1] - 4]
                        self.eggs.append([self.player.throw_egg(mouse_pos, self.current_time, self.scroll), particle.Particle(20)])

            if self.in_game:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.player_state['moving_right'] = False

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.player_state['moving_left'] = False
                    
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player_action, self.player_frame = self.animation.change_action(self.player_action, self.player_frame, "idle")

                    if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                        self.player.player_state['jumping'] = False
            
        return can_run
    

    def animate(self):
        self.player_frame += 1
        if self.player_frame >= len(self.animation.animation_data[self.player_action]):
            self.player_frame = 0
        img_name = self.animation.animation_data[self.player_action][self.player_frame]
        self.player.image = pygame.transform.flip(self.animation.all_images[img_name], self.flip, False)
    

    def decide_animation(self):
        if self.player.momentum > 0 and self.player.player_state['moving_right']:
            self.player_action, self.player_frame = self.animation.change_action(self.player_action, self.player_frame, "walk")
            self.flip = False
        if -0.3 < self.player.momentum < 0.3:
            self.player_action, self.player_frame = self.animation.change_action(self.player_action, self.player_frame, "idle")
        if self.player.momentum < 0 and self.player.player_state['moving_left']:
            self.player_action, self.player_frame = self.animation.change_action(self.player_action, self.player_frame, "walk")
            self.flip = True
        if self.player.gravity < 0 and not self.player.collision_state['bottom']:
            self.player_action, self.player_frame = self.animation.change_action(self.player_action, self.player_frame, "jump")
        if self.player.gravity > 0 and self.player.count > 5:
            self.player_action, self.player_frame = self.animation.change_action(self.player_action, self.player_frame, "fall")
        
    
    def particles(self, scroll):
        for index, [egg, particle_proccess] in enumerate(self.eggs):
            if egg.collided:
                if not egg.exploded:
                    self.play_sound(random.choice([explosion_noise, explosion_noise_1]))
                    can_launch, angle = egg.explode([self.player.rect.x + int(self.player.image.get_width()/2), self.player.rect.y + int(self.player.image.get_height()/2)])
                    self.player.launch([can_launch, angle])
                    egg.exploded = True
                    self.screen_shake += 15
                particle_proccess.smoke_explosion(self.display, [egg.collision_pos[0], egg.collision_pos[1]], 20, scroll)
                particle_proccess.dirt_explosion(self.display, [egg.collision_pos[0], egg.collision_pos[1]], 20, scroll, self.current_level[1])
                if len(particle_proccess.smoke) == 0:
                    self.eggs.pop(index)

    
    def draw_sprites(self, scroll, list):
        for sprite in list:
            self.display.blit(sprite[0].image, [sprite[0].rect.x - scroll[0], sprite[0].rect.y - scroll[1]])
    

    def update_sprites(self, current_level_tiles, delta_time, current_time, list):
        for sprite in list:
            sprite[0].update(current_level_tiles, delta_time, current_time)
        
    
    def play_sound(self, func):
        func.play()
    

    def countdown(self):
        if self.total_sec > 0:
            count_sec = self.total_sec % 60
            if count_sec < 10:
                count_sec = f"0{count_sec}"
            self.timer = f"{math.trunc(self.total_sec/60)}:{count_sec}"
            self.total_sec -= 1
            return True
        else:
            return False
    

    def reset_timer(self):
        self.total_sec = self.hours * 3600 + self.min * 60 + self.sec
        self.timer = 0            
