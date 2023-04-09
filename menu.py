import sys
import pygame.sprite
from consts import *
import button
import time
import text
import player
import load_map


class Menu:
    def __init__(self):
        self.font = text.Font('assets/fonts/small_font.png', 1)

        self.player_img = pygame.Surface((16, 16))
        self.player_img.fill((255, 255, 255))
        self.player = player.Player((130, 40), self.player_img)

        self.cursor_img = cursor_img
        self.mouse_pos = pygame.mouse.get_pos()

        self.map_loader = load_map.Load_map()

        self.Start = button.Button(40, 50, button_img, self.font, "Start")
        self.exit_button = button.Button(40, 100, button_img, self.font, "Exit")

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

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
    

    def menu(func):
        def inside(self, display, window):
            is_running = True
            while is_running:
                display.fill((255, 249, 181))

                self.mouse_pos = pygame.mouse.get_pos()

                func(self, display, window)

                self.font.render(display, str(round(self.clock.get_fps())), 10, 10)
                display.blit(self.cursor_img, (self.mouse_pos[0] / self.scale - self.change[0] - 4, self.mouse_pos[1] / self.scale - self.change[1] - 4))

                self.rescale_window(display, window)

                pygame.display.update()

                is_running = self.event_loop()

                self.clock.tick(60)
                
        return inside


    def game(self, display, window):
        is_running = True
        while is_running:
            display.fill((255, 249, 181))

            self.mouse_pos = pygame.mouse.get_pos()

            self.current_time = time.time()
            self.delta_time = self.current_time - self.previous_time
            self.delta_time *= 60
            self.previous_time = self.current_time

            self.map_loader.draw_level(self.current_level[0], display)
            self.font.render(display, str(round(self.clock.get_fps())), 10, 10)
            self.all_sprites.update(self.current_level[1], self.delta_time, self.current_time)
            self.all_sprites.draw(display)
            display.blit(self.cursor_img, (self.mouse_pos[0] / self.scale - self.change[0], self.mouse_pos[1] / self.scale - self.change[1]))

            self.rescale_window(display, window)

            pygame.display.update()

            is_running = self.event_loop()

            self.clock.tick(60)
            

    @menu
    def main_menu(self, display, window):
            display.blit(bg_img, (0, 0))
            self.font.render(display, "Main Menu", display_size[0] / 2 - 55, 20)

            if self.Start.draw(self.scale, self.change, display):
                self.current_level = [self.level_data["Level_one_data"], self.level_tiles["Level_one_tiles"]]
                self.all_sprites.remove(self.player)
                self.player = player.Player((130, 40), self.player_img)
                self.all_sprites.add(self.player)
                time.sleep(0.2)
                self.game(display, window)

            if self.exit_button.draw(self.scale, self.change, display):
                time.sleep(0.2)
                pygame.quit()
                sys.exit()
    
    
    def rescale_window(self, display, window):
        # checks how the display should scale depending on the window size.
        self.scale = min(window.get_width() / display.get_width(), window.get_height() / display.get_height())

        # changes display size to new size using scale variable.
        surf = pygame.transform.scale(display, (self.scale * display.get_width(), self.scale * display.get_height()))

        self.change = [round((window.get_width() - surf.get_width()) / 2), round((window.get_height() - surf.get_height()) / 2)]

        # Keeps display surface in the center of the window.
        window.blit(surf, (round((window.get_width() - surf.get_width()) / 2), round((window.get_height() - surf.get_height()) / 2)))
    

    def event_loop(self):
        can_run = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                click_noise.play()
                time.sleep(0.2)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.player_state['moving_right'] = True

                if event.key == pygame.K_LEFT:
                    self.player.player_state['moving_left'] = True

                if event.key == pygame.K_UP:
                    self.player.player_state['jumping'] = True

                if event.key == pygame.K_ESCAPE:
                    click_noise.play()
                    time.sleep(0.2)
                    can_run = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.player_state['moving_right'] = False

                if event.key == pygame.K_LEFT:
                    self.player.player_state['moving_left'] = False

                if event.key == pygame.K_UP:
                    self.player.player_state['jumping'] = False
            
        return can_run

                        