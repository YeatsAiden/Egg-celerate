import pygame
from pytmx.util_pygame import load_pygame


class Load_map:
    def __init__(self):
        self.level_one_data = load_pygame("assets/levels/level_1.tmx")
        # Makes a list of all the tiles in level_one_data
        self.level_one_tiles = self.make_tiles_array(self.level_one_data)

    def draw_level(self, level, surface, scroll):
        """
        Draws all the tiles for the map.

        :param level: level param is for accessing the levels tile data for blit-ing.
        :param surface: surface param is for knowing what to blit on.
        :return:
        """
        for i in level.layers:
            for x, y, surf in i.tiles():
                surface.blit(surf, (x * 8 - scroll[0], y * 8 - scroll[1]))

    def make_tiles_array(self, level):
        array = []
        for i in level.layers:
            array = [pygame.Rect(x * 8, y * 8, surf.get_width(), surf.get_height()) for x, y, surf in i.tiles()]
        return array
