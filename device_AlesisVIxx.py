# name=Alesis VIxx-2-03
# Author: ts-forgery
VERSION = '2.03'

import device
import channels
import general
from process import Process
from timing import Timing
from action import Action
from wheels import PitchWheel

def OnInit():
	"""Function called when script starts"""
	if device.isAssigned():					
		print(f"Device assigned - ver {VERSION} ")
		print(device.getName())
		print(f"Port Number: {device.getPortNumber()}")
	else:
		print(f"Not assigned - ver {VERSION}")
	print('')
	if general.getVersion() < 23:
		print('Your FL Studio version should be updated to access all features.')
		print('Versions lower than 20.8 may not work at all.')

def  OnMidiMsg(event):
	"""Function called on every midi message sent by controller"""
	process = Process(event)

def OnIdle():
	Timing.update_counter()

def OnPitchBend(event):
	Action.pitch_wheel(event)	
	# PitchWheel.process(event)
	


	





			
