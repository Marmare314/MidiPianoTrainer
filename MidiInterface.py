"""
    Class to make interfacing with a midi keyboard easier.
"""

import mido
import time
import asyncio
from collections import deque
import threading

from MidiEvent import event_from_message


class MidiInterface:
    def __init__(self, partial_name, empty_q=True):
        # find ports with partial name
        inport_name, outport_name = None, None
        for port_name in mido.get_input_names():
            if partial_name in port_name:
                inport_name = port_name
        for port_name in mido.get_output_names():
            if partial_name in port_name:
                outport_name = port_name

        # open actual midi ports
        if inport_name is not None and outport_name is not None:
            self._inport = mido.open_input(inport_name)
            self._outport = mido.open_output(outport_name)
        else:
            raise RuntimeError('Could not open partial portname: ', partial_name)

        # remove events in input queue (from prior usage)
        if empty_q:
            self.register_callback(lambda m: None)
            time.sleep(1)

        # initialize async things
        self._loop = asyncio.get_event_loop()
        self._task_q = deque()
        self._exit_clear_loop = False

        self._clear_thread = threading.Thread(target=lambda: self._loop.run_until_complete(self._clear_task_q()))
        self._clear_thread.start()

    def register_callback(self, callback):
        self._inport.callback = callback

    async def _clear_task_q(self):
        while (not self._exit_clear_loop) or (len(self._task_q) > 0):
            if len(self._task_q) > 0:
                await self._task_q.pop()
            await asyncio.sleep(0.0001)

    def play_note(self, midi_num, velocity, length, channel=1):
        self._task_q.append(self._loop.create_task(self.play_note_async(midi_num, velocity, length, channel)))

    async def play_note_async(self, midi_num, velocity, length, channel=1):
        self._outport.send(mido.Message('note_on', channel=channel - 1, note=midi_num, velocity=velocity))
        await asyncio.sleep(length)
        self._outport.send(mido.Message('note_off', channel=channel - 1, note=midi_num, velocity=velocity))

    def close(self):
        self._exit_clear_loop = True
        self._clear_thread.join()


if __name__ == '__main__':
    m = MidiInterface('CASIO USB-MIDI')
    # log events
    # m.register_callback(lambda m: print(event_from_message(m)))
    # time.sleep(10)

    from Note import Note

    Note(60).play(m, 0.6, 1)
    Note(64).play(m, 0.6, 1)
    Note(67).play(m, 0.6, 1)

    m.close()
