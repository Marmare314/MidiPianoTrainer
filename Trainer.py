"""

"""

from pygame.time import Clock, get_ticks
import random
import time

from Note import Note
from Chord import Chord
from AbstractTheoryObject import UpdateStatus
from MidiInterface import MidiInterface, event_from_message
from MusicDisplay import MusicDisplay, Coord
from MidiEvent import NoteEvent

COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (200, 255, 200)
COLOR_RED = (255, 200, 200)


class Trainer:
    def __init__(self, partial_name, trainables):
        self._midi = MidiInterface(partial_name)
        self._display = MusicDisplay((1400, 400), 300, (0, 0, 0))
        self._midi.register_callback(self.forward_callback)

        self._trainables = trainables
        self._background_color = COLOR_WHITE
        self._blink_green = False
        self._blink_green_start = None

        self._exit_note, self._replay_note = Note(21), Note(22)
        self._exit_flag = False

        self._new_active_task()

    def forward_callback(self, msg):
        msg = event_from_message(msg)
        if isinstance(msg, NoteEvent):
            if msg.is_note_on and self._exit_note == msg.note:
                self._exit_flag = True

        if self._active_task is not None:
            status = self._active_task.update(msg)
            if status == UpdateStatus.COMPLETED:
                self._blink_green = True
                time.sleep(1)
                self._new_active_task()
            elif status == UpdateStatus.PARTIAL:
                pass  # update some kind of clock to indicate that the solution is partial
            elif status == UpdateStatus.WRONG:
                self._background_color = COLOR_RED
            elif status == UpdateStatus.IGNORED:
                pass
            else:
                raise RuntimeError('Invalid status returned')

    def _new_active_task(self):
        # self._last_task = self._active_task # do this if hearing mode is active
        self._active_task = random.sample(self._trainables, 1)[0].random()

    def draw(self):
        if self._blink_green and (self._blink_green_start is None):
            self._blink_green_start = get_ticks()
            self._background_color = COLOR_GREEN
        elif self._blink_green and (get_ticks() - self._blink_green_start > 1000):
            self._background_color = COLOR_WHITE
            self._blink_green = False
            self._blink_green_start = None

        self._display.fill_screen(self._background_color)
        self._active_task.draw_name(self._display, Coord(0, 0))

    def mainloop(self):
        clock = Clock()
        while not self._exit_flag:

            # only run at 60fps to not cause too much cpu-usage
            clock.tick(60)
            self.draw()
            if self._display.update_screen():
                break


if __name__ == '__main__':
    Chord.base_notes = {Note(i) for i in range(60, 73)}
    Chord.valid_qualities = {'', 'm'}

    t = Trainer('CASIO USB-MIDI', [Chord])
    t.mainloop()