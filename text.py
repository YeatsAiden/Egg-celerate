import pygame

def clip_img(surf, x, y, width, height):
        img_copy = surf.copy()
        clip_rect = pygame.Rect(x, y, width, height)
        img_copy.set_clip(clip_rect)
        return img_copy.subsurface(img_copy.get_clip())

class Font:
    def __init__(self, path, size):
        self.font_image = pygame.image.load(path).convert()
        self.spacing = 1
        self.character_set = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        self.character_index = 0
        self.charcter_width = 0
        self.charcters = {}
        for x in range(self.font_image.get_width()):
            color = self.font_image.get_at((x, 0))
            if color == (0, 0, 255, 255):
                character_img = clip_img(self.font_image, x - self.charcter_width, 0, self.charcter_width, self.font_image.get_height())
                self.charcters[self.character_set[self.character_index]] = pygame.transform.scale(character_img, (character_img.get_width() * size, character_img.get_height() * size))
                self.charcter_width = 0
                self.character_index += 1
            else:
                 self.charcter_width += 1
    

    def render(self, surf, text, x, y):
        x_offset = 0
        for letter in text:
            if letter != ' ':
                character_img = self.charcters[letter]
                character_img.set_colorkey((0, 0, 0))
                surf.blit(character_img, (x + x_offset , y))
                x_offset += self.charcters[letter].get_width() + self.spacing
            else:
                 x_offset += 5
            
                
    


