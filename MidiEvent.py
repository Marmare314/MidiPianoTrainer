"""

"""

from collections import defaultdict
import mido

from Note import Note


class AbstractMidiEvent:
    """ Base class for Midi Events """

    def __init__(self, raw_event: mido.Message):
        self._raw_event = raw_event

    def __repr__(self) -> str:
        return str(self._raw_event)

    @property
    def time(self) -> float:
        return self._raw_event.time

    @property
    def channel(self) -> int:
        return self._raw_event.channel


class NoteEvent(AbstractMidiEvent):
    def __init__(self, raw_event: mido.Message):
        super().__init__(raw_event)

        self._is_on = True
        if raw_event.type == 'note_on':
            self._is_on = True
        elif raw_event.type == 'note_off':
            self._is_on = False
        else:
            raise ValueError('NoteEvent cannot be created from non-note message')

        self._note = Note(raw_event.note)

    def __repr__(self) -> str:
        type_str = "NoteOn" if self._is_on else "NoteOff"
        return f'NoteEvent({type_str}, {self._note}, {self.velocity})'

    @property
    def note(self) -> Note:
        """ Returns note this event refers to """
        return self._note

    @property
    def velocity(self) -> float:
        """ Returns velocity of played note """
        return self._raw_event.velocity

    @property
    def is_note_on(self) -> bool:
        """ Returns NOTE_ON or NOTE_OFF """
        return self._is_on


control_names = defaultdict(lambda: 'UNKNOWN')
control_names[64] = 'PEDAL_HOLD'
control_names[66] = 'PEDAL_SUSTENATO'
control_names[67] = 'PEDAL_SOFT'
control_names[88] = 'HIGHRES_VELOCITY'


class ControllerEvent(AbstractMidiEvent):
    def __init__(self, raw_event: mido.Message):
        super().__init__(raw_event)

        if not raw_event.is_cc():
            raise ValueError('ControllerEvent cannot be created from non-controller message')

    def __repr__(self) -> str:
        return f'ControllerEvent("{self.name}", value: {self.value})'

    @property
    def control(self) -> int:
        return self._raw_event.control

    @property
    def value(self) -> int:
        """ Returns value of this event """
        return self._raw_event.value

    @property
    def name(self) -> str:
        """ Returns midi event name """
        return control_names[self.control]


def event_from_message(midi_msg: mido.Message) -> AbstractMidiEvent:
    """ Create a subclass of abstract event from a midi message """

    if midi_msg.type == 'note_on' or midi_msg.type == 'note_off':
        return NoteEvent(midi_msg)

    if midi_msg.is_cc():
        return ControllerEvent(midi_msg)

    print('Unknown event: ', midi_msg)
    return AbstractMidiEvent(midi_msg)
