import pygame
import consts


class Button:
    def __init__(self, x, y, image, font, text):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect_pos = [x, y]
        self.rect.topleft = self.rect_pos
        self.clicked = False
        self.text = text
        self.font = font


    def draw(self, scale, change, surface):
        click = False
        # get mouse position
        pos = list(pygame.mouse.get_pos())
        pos[0], pos[1] = pos[0], pos[1]
        self.rect = pygame.Rect(self.rect_pos[0] * scale + change[0], self.rect_pos[1] * scale + change[1],
                                self.image.get_width() * scale, self.image.get_height() * scale)

        # check mouseover and clicked conditions
        if pygame.mouse.get_pressed()[0] == 1:
            self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            consts.already_pressed = False

        if self.rect.collidepoint(pos) and self.clicked and not consts.already_pressed:
            consts.click_noise.play()
            self.clicked = True
            click = True
            consts.already_pressed = True

        # draw button on screen
        surface.blit(self.image, (self.rect_pos[0], self.rect_pos[1]))
        self.font.render(surface, self.text, self.rect_pos[0] + self.image.get_width() / 4, self.rect_pos[1] + self.image.get_height() / 3)
        return click
