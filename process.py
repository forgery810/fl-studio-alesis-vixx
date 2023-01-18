# Processes midi data and sends to appropriate class

import midi
import device
from data import knob, tr_buttons
from midi import *
from turning import Knob
from switch import Switch
from pads import Pads
from wheels import ModWheel, PitchWheel
from action import Action
from config import Config

class Process:

	def __init__(self, event):
		print(event.midiId, event.data1, event.data2, event.midiChan, event.midiChanEx)																							
		self.triage(event)

	def triage(self, event):
		
		if event.midiId == 176 and event.data1 == 64 and event.midiChan == Config.SUSTAIN_CHANNEL - 1:		# ignores sustain
			pass 

		elif event.midiId == 176 and event.data1 in knob.values() and event.midiChan == 0:
			knobbb = Knob(event)	

		elif event.midiId == 144 or event.midiId == 128:
			Pads.pad_hit(event)

		elif event.midiId == 176 and event.data1 == 49 and event.midiChanEx == 128:
			ModWheel.process(event)
		
		elif event.midiId == 176 and event.data1 in tr_buttons.values() and event.data2 > 0:
			Switch.transport(event)

		elif event.midiId == 176 and event.data2 > 0:			 
			Switch.switch(event)		

		elif event.midiId == 224 and event.data2 > 0:					
			Action.pitch_wheel(event)		



