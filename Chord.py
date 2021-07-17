"""

"""

import pychord
import random

from AbstractTheoryObject import AbstractTheoryObject, UpdateStatus
from MusicDisplay import MusicDisplay, FontSize, Coord
from Note import Note


def group_extensions(extension):
    """ Group chord quality into seperate extension notes: 7b9#9 -> [7, b9, #9] """

    extension_list = []
    modifier = None

    while len(extension) > 0:
        for ext in ('-', 'b', '#', '+', 'maj', 'dim', 'sus', 'add', 'aug', 'M'):
            if extension.startswith(ext):
                extension = extension[len(ext):]
                if ext == 'M':
                    ext = 'maj'
                modifier = ext
                break

        for ext in ('min', 'm'):
            if extension.startswith(ext):
                extension_list.append(ext)
                extension = extension[len(ext):]
                break

        for ext in ('2', '4', '5', '6', '7', '9', '11', '13'):
            if extension.startswith(ext):
                if modifier:
                    extension_list.append(modifier + ext)
                    extension = extension[len(ext):]
                    modifier = None
                else:
                    extension_list.append(ext)
                    extension = extension[len(ext):]
                break

    if modifier is None:
        return extension_list
    if len(extension_list) == 0:
        return [modifier]

    raise RuntimeError('Could not group quality')


def split_extensions(grouped_extensions):
    low_text = ''
    high_text = ''

    if len(grouped_extensions) == 1:
        if grouped_extensions[0] in ('5', '6', '7', '9', '11', '13'):
            high_text += grouped_extensions[0]
        else:
            low_text += grouped_extensions[0]
    elif len(grouped_extensions) > 0:
        if grouped_extensions[0] == 'm':
            low_text = 'm'
            grouped_extensions.pop(0)
        is_first = True
        while len(grouped_extensions) > 0:
            if is_first:
                high_text += grouped_extensions.pop(0)
                is_first = False
            else:
                high_text += f'({grouped_extensions.pop(0)})'
    return low_text, high_text


class Chord(AbstractTheoryObject):
    base_notes = set()
    valid_qualities = set()
    respect_inversion = False

    chord_q = []

    def __init__(self, base_note, quality):
        self._base_note = base_note
        self._chord = pychord.Chord(base_note.key_name + quality)
        self._inversion = randint(0, len(self._chord.components()) - 1) if Chord.respect_inversion else 0
        self._name = self._base_note.random_name

    # def __eq__(self, other):
    #     if isinstance(other, ActiveKeySet):
    #         # compare without inversion
    #         if not Chord.respect_inversion:
    #             comps = {Note.from_key_name(s+'3').key_offset for s in self._chord.components()}
    #             return comps == {n.key_offset for n in other}

    #         # compare with inversion
    #         chord_notes = self.notes
    #         for i in range(self._inversion):
    #             chord_notes[i % len(chord_notes)] += 12

    #         octave_diff = min(chord_notes).octave - 3
    #         chord_notes = [note - octave_diff * 12 for note in chord_notes]

    #         return set(self.notes) == set(other)
    #     raise NotImplementedError()

    @staticmethod
    def random():
        """ Returns a random Chord, respecting settings of class """
        if len(Chord.chord_q) == 0:
            for note in Chord.base_notes:
                for qual in Chord.valid_qualities:
                    Chord.chord_q.append(Chord(note, qual))
            random.shuffle(Chord.chord_q)

        return Chord.chord_q.pop()

    def update(self, event):
        raise NotADirectoryError()

    def draw_name(self, display, position):
        low_text, high_text = split_extensions(group_extensions(self._chord.quality.quality))
        note_size, octave_size = self._base_note.draw_name(display, position, True)

        position_low_x = position + (note_size + octave_size).scale_width(self._base_note.key_name, 1.3)
        position_low_y = position + note_size.scale_height('1', 2/3)
        position_low = Coord.merge(position_low_x, position_low_y)

        position_high = position + note_size.scale_width(self._base_note.key_name, 1.2).scale_height('1', 0)

        display.draw_text(low_text, position_low, FontSize.MEDIUM)
        display.draw_text(high_text, position_high, FontSize.MEDIUM)

    def draw_notation(self, display, position):
        raise NotImplementedError()

    # @property
    # def notes(self):
    #     """ Returns a list of note starting in octave 3 """
    #     chord_notes = [Note.from_key_name(s) for s in self._chord.components_with_pitch(3)]
    #     for i in range(self._inversion):
    #         chord_notes[i % len(chord_notes)] += 12

    #     octave_diff = min(chord_notes).octave - 3
    #     return [note - octave_diff * 12 for note in chord_notes]

    # @property
    # def name(self):
    #     """ Returns a random variation of the name of the base note """
    #     return self._name

    # @property
    # def quality(self) -> str:
    #     """ Returns quality of chord """
    #     return self._chord.quality.quality

    # @property
    # def inversion(self) -> int:
    #     return self._inversion


if __name__ == '__main__':
    Chord.base_notes.add(Note(60))
    Chord.valid_qualities.add('mM7')

    d = MusicDisplay((640, 480), 200, (0, 0, 0))
    d.fill_screen((255, 255, 255))
    c = Chord.random()
    c.draw_name(d, Coord(0, 0))
    while True:
        if d.update_screen():
            break
