import pygame
pygame.mixer.init()

window_size = (960, 640)
display_size = (240, 160)

bg_img = pygame.transform.scale(pygame.image.load("assets/sprites/Background.png"), display_size)
sea_img = pygame.transform.scale(pygame.image.load("assets/sprites/sea.png"), display_size)
sun_img = pygame.transform.scale(pygame.image.load("assets/sprites/sun.png"), display_size)
sky_img = pygame.transform.scale(pygame.image.load("assets/sprites/sky.png"), display_size)
sky_1_img = pygame.transform.scale(pygame.image.load("assets/sprites/sky_1.png"), display_size)
bg_game_img = pygame.transform.scale(pygame.image.load("assets/sprites/bg_img.png"), display_size)
game_over_img = pygame.transform.scale(pygame.image.load("assets/sprites/Game_over.png"), display_size)
button_img = pygame.image.load("assets/sprites/Button.png")
cursor_img = pygame.image.load("assets/sprites/cursor.png")
egg_img = pygame.image.load("assets/sprites/egg.png")
transparent_egg_img = pygame.image.load("assets/sprites/transparent_egg.png")
smoke_img = pygame.image.load("assets/sprites/smoke.png")
sparkle_img = pygame.image.load("assets/sprites/sparkle.png")
sparkle_1_img = pygame.image.load("assets/sprites/sparkle_1.png")
dirt_img = pygame.image.load("assets/sprites/dirt.png")
finish_img = pygame.image.load("assets/sprites/finish.png")

jump_noise = pygame.mixer.Sound("assets/sounds/jump.wav")
jump_noise.set_volume(0.3)
click_noise = pygame.mixer.Sound("assets/sounds/click.wav")
click_noise.set_volume(0.5)
explosion_noise = pygame.mixer.Sound("assets/sounds/explosion.wav")
explosion_noise.set_volume(0.5)
explosion_noise_1 = pygame.mixer.Sound("assets/sounds/explosion_1.wav")
explosion_noise_1.set_volume(0.5)
game_over_noise = pygame.mixer.Sound("assets/sounds/game_over.wav")
game_over_noise.set_volume(0.7)
win_noise = pygame.mixer.Sound("assets/sounds/win.wav")
win_noise.set_volume(0.7)


g = 9.807/2000  # divide to make it less quick

already_pressed = False
