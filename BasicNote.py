"""

"""

import random


class BasicNote:
    """ Represents a unique note on keyboard [A-1, C7] """

    KEY_RANGE = (21, 108)

    def __init__(self, midi_num):
        if BasicNote.KEY_RANGE[0] <= midi_num <= BasicNote.KEY_RANGE[1]:
            self._key_offset = midi_num % 12
            self._octave = midi_num // 12 - 2
        else:
            raise ValueError('Midi keynumber should be in [0, 127]')

    def __eq__(self, other: object):
        if isinstance(other, BasicNote):
            return self._key_offset == other._key_offset and self._octave == other._octave
        return False

    @property
    def octave(self):
        return self._octave

    @property
    def key_offset(self):
        return self._key_offset

    @staticmethod
    def random():
        return BasicNote(random.randint(*BasicNote.KEY_RANGE))
