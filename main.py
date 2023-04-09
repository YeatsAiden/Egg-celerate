import pygame
from pygame import *
from menu import *
from load_map import *

pygame.init()
window = pygame.display.set_mode(window_size, RESIZABLE)
display = pygame.Surface(display_size)
pygame.mouse.set_visible(False)

main_menu = Menu()

main_menu.main_menu(display, window)
