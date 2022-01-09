# Processes midi data and sends to appropriate class


import midi
import device
from data import button, mode, parameters, knob
from midi import *
from turning import Knob, mapvalues
import switch
import notes


toggle_switches = [49, 81, 89, 114, 115]

class Process:

	def __init__(self, event):
		print(event.midiId, event.data1, event.data2, event.midiChan)																							
		self.event = event
		self.triage(event)

	def triage(self, event):

		if event.data1 not in knob.values():
			if event.midiId == 144:
				notes.Pads.pad_hit(event)
		
			elif event.midiId == 176 and event.data1 not in toggle_switches and event.data2 > 0:			 
				switch.Switch.switch_moment(event)		

			elif event.midiId == 224 and event.data2 > 0:							
				switch.Switch.switch_moment(event)		
	
			elif event.midiId == 176 and event.data1 in toggle_switches and event.midiId == midi.MIDI_CONTROLCHANGE:
				switch.Switch.switch_toggle(event)

		elif event.midiId == 176 and event.data1 in knob.values():
			knobbb = Knob(event)		
			# event.handled = True

