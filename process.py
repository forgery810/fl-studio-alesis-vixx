# Processes midi data and sends to appropriate class

import midi
import device
from data import button, mode, parameters, knob
from midi import *
from turning import Knob, mapvalues
from switch import Switch
from notes import Pads

toggle_switches = [49, 81, 89, 114, 115]

class Process:

	def __init__(self, event):
		print(event.midiId, event.data1, event.data2, event.midiChan, event.midiChanEx)																							
		self.event = event
		self.triage(event)

	def triage(self, event):
		"""takes midi event data and sends to appropriate class or function"""
		if event.data1 not in knob.values():
			if event.midiId == 144 or event.midiId == 128:
				Pads.pad_hit(event)
		
			elif event.midiId == 176 and event.data1 not in toggle_switches and event.data2 > 0:			 
				Switch.switch_moment(event)		

			elif event.midiId == 224 and event.data2 > 0:							
				Switch.switch_moment(event)		
	
			elif event.midiId == 176 and event.data1 in toggle_switches and event.midiId == midi.MIDI_CONTROLCHANGE:
				Switch.switch_toggle(event)

		elif event.midiId == 176 and event.data1 in knob.values():
			knobbb = Knob(event)		

