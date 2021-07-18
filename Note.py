"""

"""

import random

from AbstractTheoryObject import AbstractTheoryObject, UpdateStatus
from MidiEvent import NoteEvent
from BasicNote import BasicNote
from MusicDisplay import MusicDisplay, FontSize, Coord


class Note(AbstractTheoryObject):

    keys_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    keys_b = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    default_scale = keys_b
    random_name = False

    def __init__(self, midi_num):
        if isinstance(midi_num, BasicNote):
            self._note = midi_num
        elif isinstance(midi_num, int):
            self._note = BasicNote(midi_num)
        else:
            raise TypeError('Note can only be constructed from BasicNote and int')
        self._set_key_name()

    def __eq__(self, other):
        if isinstance(other, Note):
            return self._note == other._note
        elif isinstance(other, BasicNote):
            return self._note == other
        return False

    def __hash__(self):
        return hash(self._note)

    def __add__(self, other):
        if isinstance(other, int):
            return Note(self._note.midi_num + other)
        raise TypeError('Can only add int to Note')

    def _set_key_name(self):
        scale = Note.default_scale
        if Note.random_name:
            # TODO: add more scales (Dbb, C##)
            scale = random.sample([Note.keys_b, Note.keys_sharp], 1)[0]
        self._key_name = scale[self._note.key_offset]

    @property
    def key_name(self):
        return self._key_name

    @staticmethod
    def random():
        return Note(BasicNote.random())

    def update(self, event):
        if isinstance(event, NoteEvent) and event.is_note_on:
            if self == event.note:
                return UpdateStatus.COMPLETED
            return UpdateStatus.WRONG

    def draw_name(self, display, position, show_octave):
        size_name = display.draw_text(self.key_name, position, FontSize.BIG)

        if show_octave:
            position_octave = size_name.scale_width(self.key_name, 0.2) + position
            size_octave = display.draw_text(str(self._note.octave), position_octave, FontSize.SMALL)
            return size_name, size_octave
        return size_name

    def draw_notation(self, display, position):
        # TODO: draw note on musical lines
        pass

    def play(self, midi, velocity, length, channel=1):
        if 0 <= velocity <= 1 and 1 <= channel <= 16 and length > 0:
            midi.play_note(self._note.midi_num, int(velocity * 127), length, channel)


if __name__ == '__main__':
    # TODO: also test draw
    d = MusicDisplay((640, 480), 200, (0, 0, 0))
    d.fill_screen((255, 255, 255))
    n = Note(60)
    n.draw_name(d, Coord(0, 0), True)
    while True:
        if d.update_screen():
            break
