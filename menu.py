import sys
import pygame.sprite
from consts import *
import button
import time
import text
import player
import flag
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

        self.flag = flag.Flag([120, 48])

        self.trail = particle.Particle(1)
        self.stars = particle.Particle(1)

        self.cursor_img = cursor_img
        self.mouse_pos = pygame.mouse.get_pos()

        self.map_loader = load_map.Load_map()

        self.Start = button.Button(10, 5, button_img, self.font, "Start")
        self.Exit_button = button.Button(10, 25, button_img, self.font, "Exit")
        self.Menu = button.Button(10, 25, button_img, self.font, "Menu")
        self.Continue = button.Button(10, 45, button_img, self.font, "Continue")

        self.all_sprites = []
        self.eggs = []

        self.level_tiles = {
            "Level_one_tiles": self.map_loader.level_one_tiles
        }

        self.level_data = {
            "Level_one_data": self.map_loader.level_one_data
        }

        self.current_level = [self.level_data["Level_one_data"], self.level_tiles["Level_one_tiles"]]

        self.bg_imgs = {
            "bg": bg_img,
            "game_over": game_over_img,
        }

        self.current_bg_img = self.bg_imgs['bg']

        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.delta_time = 0

        self.scale = 1
        self.change = [0, 0]

        self.current_time = time.time()
        self.previous_time = time.time()

        self.scroll = [0, 0]
        self.scroll_k = [0.1, 0.1, 0.05]
        self.tile_scroll = [0, 0]

        self.in_game = False
        self.paused = False

        self.timer = 0
        self.best_time = f'{math.trunc(self.get_record()/60)}:{(self.get_record()%60-1) if self.get_record()%60 > 10 else "0"+self.get_record()%60-1}'
        self.hours = 0
        self.min = 2
        self.sec = 30
        self.total_sec = self.hours * 3600 + self.min * 60 + self.sec
        self.total_time = self.hours * 3600 + self.min * 60 + self.sec

        self.count_down_event = pygame.event.custom_type()
        pygame.time.set_timer(self.count_down_event, 1000)

        self.screen_shake = 0
        self.win = False

        pygame.mixer.music.load("assets/music/silly_song.wav")
        pygame.mixer.music.set_volume(0.7)
    

    def menu(func):
        def inside(self):
            is_running = True
            while is_running:
                self.display.fill((255, 249, 181))

                self.mouse_pos = pygame.mouse.get_pos()

                func(self)

                self.display.blit(self.cursor_img, (self.mouse_pos[0] / self.scale - 4, self.mouse_pos[1] / self.scale - 4))

                self.rescale_window()

                pygame.display.update()

                is_running = self.event_loop(is_running)

                self.clock.tick(60)
                
        return inside


    def game(self):
        is_running = True
        self.in_game = True
        self.win = False
        self.flag.collision = False
        self.confetti = particle.Particle(30)
        self.scroll = [0, 0]
        self.reset_timer()
        self.current_level = [self.level_data["Level_one_data"], self.level_tiles["Level_one_tiles"]]
        self.all_sprites.clear()
        self.eggs.clear()
        self.player = player.Player((120, 3900), self.player_img)
        self.all_sprites.append([self.player, 0])
        pygame.mixer.music.play(-1)
        while is_running:
            self.display.fill((160, 124, 167))

            self.mouse_pos = pygame.mouse.get_pos()

            self.current_time = time.time()
            self.previous_time = self.current_time

            if self.screen_shake > 0:
                self.screen_shake -= 1
            
            self.scroll[0] = 0

            if self.screen_shake:
                self.scroll[0] += random.randint(0, 10) - 5
                self.scroll[1] += random.randint(0, 10) - 5

            self.scroll[1] += (self.player.rect.y - self.scroll[1] - display_size[1]/2)/20
            self.tile_scroll = [int(self.scroll[0]), int(self.scroll[1])+2]

            self.decide_animation()
            self.animate()

            self.draw_bg(self.scroll)
            self.map_loader.draw_level(self.current_level[0], self.display, self.tile_scroll)
            self.flag.draw(self.display, self.scroll)
            self.draw_sprites(self.scroll, self.all_sprites)
            self.draw_sprites(self.scroll, self.eggs)
            self.trail.trail(self.display, self.player.rect.topleft, 10, self.scroll, 8, 12)
            self.particles(self.scroll)
            self.font.render(self.display, f'Height: {self.player.height}', 180, 10)
            self.font.render(self.display, f'Time: {self.timer}', 180, 20)
            self.display.blit(self.cursor_img, (self.mouse_pos[0] / self.scale - 4, self.mouse_pos[1] / self.scale - 4))

            self.update_sprites(self.current_level[1], self.delta_time, self.current_time, self.all_sprites)
            self.update_sprites(self.current_level[1], self.delta_time, self.current_time, self.eggs)
            self.win = self.flag.check_collision(self.player.rect)

            if self.win:
                self.confetti.confetti_explosion(self.display, self.flag.rect.topleft, 30, self.scroll, self.current_level[1])
                self.font.render(self.display, 'You Won!', 110, 40)
                if not len(self.confetti.confetti):
                    is_running = False

            self.rescale_window()

            pygame.display.update()

            is_running = self.event_loop(is_running)
            self.can_launch = False

            self.clock.tick(60)
        pygame.mixer.music.stop()
        if self.win:
            self.calc_best_time()
        
            

    @menu
    def main_menu(self):
            self.in_game = False
            self.current_bg_img = self.bg_imgs['bg']
            self.display.blit(self.current_bg_img, (0, 0))
            self.font.render(self.display, "Main Menu", 155, 10)
            self.font.render(self.display, f"Best Time {self.best_time}", 155, 30)

            if self.Start.draw(self.scale, self.change, self.display):
                time.sleep(0.2)
                self.game()

            if self.Exit_button.draw(self.scale, self.change, self.display):
                time.sleep(0.2)
                pygame.quit()
                sys.exit()
            
    
    def pause_menu(self):
            pygame.mixer.music.stop()
            is_running = True
            self.paused = True
            self.in_game = False
            self.current_bg_img = self.bg_imgs['bg']
            while is_running:
                self.display.fill((255, 249, 181))

                self.mouse_pos = pygame.mouse.get_pos()

                self.display.blit(self.current_bg_img, (0, 0))
                self.font.render(self.display, "Pause Menu", 155, 10)

                if self.Menu.draw(self.scale, self.change, self.display):
                    time.sleep(0.2)
                    self.in_game = False
                    return False
                    
                if self.Continue.draw(self.scale, self.change, self.display):
                    time.sleep(0.2)
                    pygame.mixer.music.play(-1)
                    self.in_game = True
                    return True

                self.display.blit(self.cursor_img, (self.mouse_pos[0] / self.scale - 4, self.mouse_pos[1] / self.scale - 4))

                self.rescale_window()

                pygame.display.update()

                is_running = self.event_loop(is_running)

                self.clock.tick(60)
                
    
    def rescale_window(self):
        # checks how the display should scale depending on the window size.
        self.scale = min(self.window.get_width() / self.display.get_width(), self.window.get_height() / self.display.get_height())

        # changes display size to new size using scale variable.
        surf = pygame.transform.scale(self.display, (self.scale * self.display.get_width(), self.scale * self.display.get_height()))

        self.change = [round((self.window.get_width() - surf.get_width()) / 2), round((self.window.get_height() - surf.get_height()) / 2)]

        # Keeps display surface in the center of the window.
        self.window.blit(surf, (self.change[0], self.change[1]))
    

    def event_loop(self, is_running):
        can_run = is_running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_noise.play()
                time.sleep(0.2)
                pygame.quit()
                sys.exit()

            if self.in_game and not self.win:
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
                        can_run = self.pause_menu()

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
    

    def calc_best_time(self):
        time = self.get_record()
        time_diff = self.total_time - self.total_sec
        if time_diff < time:
            time = time_diff
            self.save_time(time)
        min_diff = time / 60
        sec_diff = time % 60
        if sec_diff < 10:
            sec_diff = f"0{sec_diff}"
        self.best_time = f"{math.trunc(min_diff)}:{sec_diff}"
    

    def save_time(self, time):
        with open("assets/record/record.txt", 'w') as f:
            f.write(str(time))
    

    def get_record(self):
        with open("assets/record/record.txt", 'r') as f:
            time = int(f.read())
        return time
    

    def reset_timer(self):
        self.total_sec = self.hours * 3600 + self.min * 60 + self.sec
        self.timer = 0          


    def draw_bg(self, scroll):
        self.display.blit(sky_1_img, (0, 0))
        self.stars.trail(self.display, [0, 0], 30, [0, 0], display_size[0], display_size[1])
        self.display.blit(sky_img, (0, 0 - scroll[1] * self.scroll_k[2] + 200))
        self.display.blit(sun_img, (0, 0 - scroll[1] * self.scroll_k[1] + 375))
        self.display.blit(sea_img, (0, 0 - scroll[1] * self.scroll_k[0] + 375))
