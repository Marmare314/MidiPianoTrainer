"""
    Class to make interfacing with a midi keyboard easier.
"""

import mido
import time

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

    def register_callback(self, callback):
        self._inport.callback = callback


if __name__ == '__main__':
    m = MidiInterface('CASIO USB-MIDI')
    m.register_callback(lambda m: print(event_from_message(m)))
    time.sleep(10)
