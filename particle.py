import pygame
from consts import *
import random

class Particle:
    def __init__(self, duration):
        self.smoke = []
        self.dirt = []
        self.sparkle = []
        self.confetti = []
        self.repetitions = [True for frame in range(duration)]
        self.repetition_index = 0
        self.repetition_index_1 = 0
        self.can_append = True
        self.size = 1
        self.width = 1
        self.brightness = 238
        self.color = (self.brightness, self.brightness, self.brightness)
        self.colors = [(234, 114, 134), (227, 225, 159), (169, 196, 132), (93, 147, 123), (244, 164, 191), (163, 178, 210)]

    def smoke_explosion(self, surf, pos, duration, scroll):
        if self.can_append:
            self.smoke.append([[pos[0] + random.randint(0, 16) - 8, pos[1] + random.randint(0, 8) - 4], [random.randint(-10, 10)/10, random.randint(-10, 0)/10], duration, self.color, self.brightness])
        if self.repetition_index >= len(self.repetitions):
            self.can_append = False
            self.repetition_index = 0
        if self.repetitions[self.repetition_index] or len(self.smoke) > 0:
            for particle in self.smoke:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= 0.4
                particle[3] = (particle[4], particle[4], particle[4])
                img = self.chang_color(pygame.transform.scale(smoke_img, [particle[2], particle[2]]), particle[3])
                surf.blit(img, (particle[0][0] - scroll[0], particle[0][1] - scroll[1]))
                pygame.draw.circle(surf, (119, 127, 143), [pos[0] - scroll[0], pos[1] - scroll[1]], self.size, 5 )
                if particle[4] >= 150:
                    particle[4] -= 5 
                if particle[2] <= 0:
                    self.smoke.remove(particle)
        self.repetition_index += 1
        self.size += 5
    
    def dirt_explosion(self, surf, pos, duration, scroll, tiles):
        if self.can_append:
            self.dirt.append([[pos[0] + random.randint(0, 16) - 8, pos[1] + random.randint(0, 8) - 4], [random.randint(-30, 30)/10, random.randint(-30, 0)/10], duration, random.randint(2, 6), pygame.Rect(pos[0], pos[1], 1, 1)])
        if self.repetition_index_1 >= len(self.repetitions):
            self.can_append = False
            self.repetition_index_1 = 0
        if self.repetitions[self.repetition_index_1] or len(self.dirt):
            for particle in self.dirt:
                particle[0][0] += particle[1][0]
                particle[4].x = particle[0][0]
                for tile in tiles:
                    if tile.colliderect(particle[4]):
                        particle[1][0] *= -0.5
                        particle[0][0] += particle[1][0] * 2
                particle[0][1] += particle[1][1]
                particle[1][1] += 0.1
                particle[4].y = particle[0][1]
                for tile in tiles:
                    if tile.colliderect(particle[4]):
                        particle[1][1] *= -0.4
                        particle[0][1] += particle[1][1] * 2
                particle[2] -= 0.1
                particle[3] -= 0.04
                if particle[3] < 0:
                    particle[3] = 0
                img = pygame.transform.scale(dirt_img, [particle[3], particle[3]])
                surf.blit(img, (particle[0][0] - scroll[0], particle[0][1] - scroll[1]))
                if particle[2] <= 0:
                    self.dirt.remove(particle)
        self.repetition_index_1 += 1
    

    def trail(self, surf, pos, duration, scroll, width, height):
        if len(self.sparkle) <= 5:
            self.sparkle.append([[pos[0] + random.randint(0, width), pos[1] + random.randint(0, height)], [random.randint(-20, 20)/10, random.randint(-20, 20)/10], duration, random.choice([sparkle_1_img, sparkle_img])])
        for particle in self.sparkle:
            particle[2] -= 1
            img = pygame.transform.scale(particle[3], [1, 1])
            surf.blit(img, (particle[0][0] - scroll[0], particle[0][1] - scroll[1]))
            if particle[2] <= 0:
                self.sparkle.remove(particle)
    

    def confetti_explosion(self, surf, pos, duration, scroll, tiles):
        if self.can_append:
            self.confetti.append([[pos[0] + random.randint(0, 16) - 8, pos[1] + random.randint(0, 8) - 4], [random.randint(-20, 20)/10, random.randint(-50, 0)/10], duration, random.randint(2, 8), pygame.Rect(pos[0], pos[1], 1, 1), random.choice(self.colors)])
        if self.repetition_index_1 >= len(self.repetitions):
            self.can_append = False
            self.repetition_index_1 = 0
        if self.repetitions[self.repetition_index_1] or len(self.confetti):
            for particle in self.confetti:
                particle[0][0] += particle[1][0]
                particle[4].x = particle[0][0]
                for tile in tiles:
                    if tile.colliderect(particle[4]):
                        particle[1][0] *= -0.5
                        particle[0][0] += particle[1][0] * 2
                particle[0][1] += particle[1][1]
                particle[1][1] += 0.1
                particle[4].y = particle[0][1]
                for tile in tiles:
                    if tile.colliderect(particle[4]):
                        particle[1][1] *= -0.4
                        particle[0][1] += particle[1][1] * 2
                particle[2] -= 0.1
                particle[3] -= 0.01
                if particle[3] < 0:
                    particle[3] = 0
                img = self.chang_color(pygame.transform.scale(smoke_img, [particle[3], particle[3]]), particle[5])
                surf.blit(img, (particle[0][0] - scroll[0], particle[0][1] - scroll[1]))
                if particle[2] <= 0:
                    self.confetti.remove(particle)
        self.repetition_index_1 += 1
        
        
    def chang_color(self, image, color):
        color_img = pygame.Surface(image.get_size())
        color_img.fill(color)
        
        image = image.copy()
        image.blit(color_img, (0, 0), special_flags = pygame.BLEND_MULT)
        return image
            