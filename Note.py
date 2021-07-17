"""

"""

import random

from AbstractTheoryObject import AbstractTheoryObject, UpdateStatus
from MidiEvent import NoteEvent
from BasicNote import BasicNote
from MusicDisplay import MusicDisplay, FontSize


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

    def __eq__(self, other: object):
        if isinstance(other, Note):
            return self._note == other._note
        return False

    def _set_key_name(self):
        scale = Note.default_scale
        if Note.random_name:
            # TODO: add more scales (Dbb, C##)
            scale = random.sample([Note.keys_b, Note.keys_sharp], 1)[0]
        self._key_name = random.sample(scale, 1)[0]

    @staticmethod
    def random():
        return Note(BasicNote.random())

    def update(self, event):
        if isinstance(event, NoteEvent) and event.is_note_on:
            if self == event.note:
                return UpdateStatus.COMPLETED
            return UpdateStatus.WRONG

    def draw(self, display, position) -> None:
        # TODO: draw note on musical lines
        pass

    def draw_name(self, display, position, show_octave):
        size_name = display.draw_text(self._key_name, position, FontSize.BIG)

        if show_octave:
            position_octave = (position[0] + int((1 + 0.2 / len(self._key_name)) * size_name[0]), position[1] + size_name[1])
            size_octave = display.draw_text(str(self._note.octave), position_octave, FontSize.SMALL)
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
