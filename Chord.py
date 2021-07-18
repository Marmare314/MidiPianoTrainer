"""

"""

from pychord.constants.qualities import DEFAULT_QUALITIES
import random

from AbstractTheoryObject import AbstractTheoryObject, UpdateStatus
from MusicDisplay import MusicDisplay, FontSize, Coord
from Note import Note
from MidiEvent import NoteEvent


quality_pitches = {q: p for q, p in DEFAULT_QUALITIES}


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
        self._quality = quality
        self._inversion = randint(0, len(self._chord.components()) - 1) if Chord.respect_inversion else 0
        self._name = self._base_note.random_name

        self._played_keys = set()
        self._set_notes()

    def _set_notes(self):
        # TODO: respect inversion, and shift to around C3
        self._notes = set()
        for pitch in quality_pitches[self._quality]:
            self._notes.add(self._base_note + pitch)

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
        if isinstance(event, NoteEvent):
            if event.is_note_on:
                if event.note in self._notes:
                    self._played_keys.add(event.note)
                    if self._played_keys == self._notes:
                        return UpdateStatus.COMPLETED
                    return UpdateStatus.PARTIAL
                else:
                    self._played_keys.add(event.note)
                    return UpdateStatus.WRONG
            else:
                if event.note in self._played_keys:
                    self._played_keys.remove(event.note)
                return UpdateStatus.WRONG
        return UpdateStatus.IGNORED

    def draw_name(self, display, position):
        low_text, high_text = split_extensions(group_extensions(self._quality))
        note_size, octave_size = self._base_note.draw_name(display, position, True, self._inversion)

        position_low_x = position + (note_size + octave_size).scale_width(self._base_note.key_name, 0.3)
        position_low_y = position + note_size.scale_height('1', 2/3)
        position_low = Coord.merge(position_low_x, position_low_y)

        position_high = position + note_size.scale_width(self._base_note.key_name, 0.2).scale_height('1', 0)

        display.draw_text(low_text, position_low, FontSize.MEDIUM)
        display.draw_text(high_text, position_high, FontSize.MEDIUM)

    def draw_notation(self, display, position):
        raise NotImplementedError()

    def play(self, midi, velocity, length, channel=1, wait_time=0):
        for note in self._notes:
            note.play(midi, velocity, length, channel, wait_time)


if __name__ == '__main__':
    Chord.base_notes.add(Note(61))
    Chord.valid_qualities.add('mM7')

    d = MusicDisplay((640, 480), 200, (0, 0, 0))
    d.fill_screen((255, 255, 255))
    c = Chord.random()
    c.draw_name(d, Coord(0, 0))
    while True:
        if d.update_screen():
            break
