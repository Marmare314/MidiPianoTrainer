"""

"""

from __future__ import annotations
from typing import Tuple

from AbstractTheoryObject import AbstractTheoryObject, UpdateStatus
from MusicDisplay import MusicDisplay, FontSize

import random


class Note(AbstractTheoryObject):
    """ Represents a unique note on keyboard [A-1, C7] """

    KEY_RANGE = (21, 108)
    keys_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    keys_b = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    default_scale = keys_b
    random_name = False

    def __init__(self, midi_num: int):
        if Note.KEY_RANGE[0] <= midi_num <= Note.KEY_RANGE[1]:
            self._key_offset = midi_num % 12
            self._octave = midi_num // 12 - 2
            self._set_key_name()
        else:
            raise ValueError('Midi keynumber should be in [0, 127]')

    def _set_key_name(self) -> None:
        scale = Note.default_scale
        if Note.random_name:
            # TODO: add more scales (Dbb, C##)
            scale = random.sample([Note.keys_b, Note.keys_sharp], 1)[0]
        self._key_name = random.sample(scale, 1)[0]

    @staticmethod
    def random() -> Note:
        return Note(random.randint(*Note.KEY_RANGE))

    def update(self, event: AbstractMidiEvent) -> UpdateStatus:
        raise NotImplementedError()

    def draw(self, display: MusicDisplay, position: Tuple[int, int]) -> None:
        # TODO: draw note on musical lines
        pass

    def draw_name(self, display: MusicDisplay, position: Tuple[int, int], show_octave: bool) -> Tuple[int, int]:
        size_name = display.draw_text(self._key_name, position, FontSize.BIG)

        if show_octave:
            position_octave = (position[0] + int((1 + 0.2 / len(self._key_name)) * size_name[0]), position[1] + size_name[1])
            size_octave = display.draw_text(str(self._octave), position_octave, FontSize.SMALL)
            return (size_name[0] + size_octave[0], size_name[1] + size_octave[1])
        return size_name


if __name__ == '__main__':
    d = MusicDisplay((640, 480), 200, (0, 0, 0))
    d.fill_screen((255, 255, 255))
    n = Note(60)
    n.draw_name(d, (0, 0), True)
    while True:
        if d.update_screen():
            break
