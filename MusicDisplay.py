"""
    Class to make displaying Notes/Chords/... easier.
"""

from __future__ import annotations
from typing import Tuple

import pygame
import enum


class Coord:
    def __init__(self, width, height):
        self._width = int(width)
        self._height = int(height)

    def __add__(self, other):
        if isinstance(other, Coord):
            return Coord(self._width + other._width, self._height + other._height)

    def scale_width(self, text, factor):
        return Coord(self._width * (1 + factor / len(text)), self._height)

    def scale_height(self, text, factor):
        return Coord(self._width, self._height * factor / len(text))

    @staticmethod
    def merge(x, y):
        return Coord(x._width, y._height)

    @property
    def tup(self):
        return (self._width, self._height)


class FontSize(enum.IntEnum):
    SMALL = 0
    MEDIUM = 1
    BIG = 2


class MusicDisplay:
    def __init__(self, dimensions, font_size, font_color):
        pygame.init()
        self._screen = pygame.display.set_mode(dimensions)

        self._dimensions = dimensions
        self._font_color = font_color
        self.font_size = font_size

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, new_size):
        self._font_size = new_size
        self._fonts = {
            FontSize.BIG: pygame.font.SysFont('Courier', new_size),
            FontSize.MEDIUM: pygame.font.SysFont('Courier', new_size // 2),
            FontSize.SMALL: pygame.font.SysFont('Courier', new_size // 3),
        }

    def draw_text(self, text, position, font_size):
        text_surface = self._fonts[font_size].render(text, True, self._font_color)
        text_bounds = text_surface.get_bounding_rect()

        self._screen.blit(text_surface, position.tup)

        return Coord(text_bounds[2], text_bounds[3])

    def fill_screen(self, color):
        self._screen.fill(color)

    def update_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        pygame.display.update()
        return False


if __name__ == '__main__':
    d = MusicDisplay((640, 480), 200, (0, 0, 0))
    d.fill_screen((255, 255, 255))
    d.draw_text('Hallo Welt!', (0, 0), FontSize.SMALL)
    while True:
        if d.update_screen():
            break
