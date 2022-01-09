# name=Alesis VIxx-1.50
# Author: ts-forgery
# Version 1.5



import device
import channels
from process import Process
from notes import Pads




	# Function called when script starts

def OnInit():


	if device.isAssigned():					# check if device assigned
		print("Device assigned - ver 1.50")
		print(device.getName())
		print("Port Number:")
		print(device.getPortNumber())
	else:
		print("Not assigned - ver 1.50")

	pad = Pads()


	# Function called on every midi message

def  OnMidiMsg(event):
	process = Process(event)


	# Function called on every beat

def OnUpdateBeatIndicator(event):
	pass






def num_gen():
	rand_obj = _random.Random()
	rand_obj.seed()
	rand_int = rand_obj.getrandbits(16) 
	return rand_int 


def PlayChannel(note, vel):												
	channels.selectOneChannel(note-60)
	channels.midiNoteOn(note-60, 60, vel)

			
