import pygame
pygame.mixer.init()

window_size = (960, 640)
display_size = 480, 320

bg_img = pygame.image.load("assets/sprites/Background.png")
button_img = pygame.image.load("assets/sprites/Button.png")
cursor_img = pygame.image.load("assets/sprites/cursor.png")

jump_noise = pygame.mixer.Sound("assets/sounds/jump.wav")
jump_noise.set_volume(0.3)
click_noise = pygame.mixer.Sound("assets/sounds/click.wav")
click_noise.set_volume(0.5)
g = 9.807/2000  # divide to make it less quick

already_pressed = False
