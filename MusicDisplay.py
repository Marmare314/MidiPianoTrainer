"""
    Class to make displaying Notes/Chords/... easier.
"""

from __future__ import annotations
from typing import Tuple

import pygame
import enum


class FontSize(enum.IntEnum):
    SMALL = 0
    MEDIUM = 1
    BIG = 2


class MusicDisplay:
    def __init__(self, dimensions: Tuple[int, int], font_size: int, font_color: Tuple[int, int, int]):
        pygame.init()
        self._screen = pygame.display.set_mode(dimensions)

        self._dimensions = dimensions
        self._font_color = font_color
        self.font_size = font_size

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, new_size: int) -> None:
        self._font_size = new_size
        self._fonts = {
            FontSize.BIG: pygame.font.SysFont('Courier', new_size),
            FontSize.MEDIUM: pygame.font.SysFont('Courier', new_size // 2),
            FontSize.SMALL: pygame.font.SysFont('Courier', new_size // 3),
        }

    def draw_text(self, text: str, position: Tuple[int, int], font_size: FontSize) -> Tuple[int, int]:
        text_surface = self._fonts[font_size].render(text, True, self._font_color)
        text_bounds = text_surface.get_bounding_rect()

        self._screen.blit(text_surface, position)

        return (text_bounds[2], text_bounds[3])

    def fill_screen(self, color: Tuple[int, int, int]) -> None:
        self._screen.fill(color)

    def update_screen(self) -> bool:
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
