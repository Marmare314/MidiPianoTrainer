"""

"""

from __future__ import annotations
from typing import Tuple

import enum

from MusicDisplay import MusicDisplay
from MidiEvent import AbstractMidiEvent


class UpdateStatus(enum.IntEnum):
    COMPLETED = 0
    PARTIAL = 1
    WRONG = 2


class AbstractTheoryObject:
    def __init__(self):
        pass

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()

    @staticmethod
    def random() -> AbstractTheoryObject:
        raise NotImplementedError()

    def update(self, event: AbstractMidiEvent) -> UpdateStatus:
        raise NotADirectoryError()

    def draw(self, display: MusicDisplay, position: Tuple[int, int]) -> None:
        pass
