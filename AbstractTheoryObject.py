"""

"""

import enum


class UpdateStatus(enum.IntEnum):
    COMPLETED = 0
    PARTIAL = 1
    WRONG = 2
    IGNORED = 3


class AbstractTheoryObject:
    @staticmethod
    def random():
        raise NotImplementedError()

    def update(self, event):
        raise NotADirectoryError()

    def draw_name(self, display, position):
        raise NotImplementedError()

    def draw_notation(self, display, position):
        raise NotImplementedError()

    def play(midi, velocity, length, channel=1):
        raise NotImplementedError()
