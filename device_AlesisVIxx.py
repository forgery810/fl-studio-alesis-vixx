# name=Alesis VIxx-1.54
# Author: ts-forgery
# Version 1.54

import device
import channels
from process import Process

def OnInit():
	"""Function called when script starts"""
	if device.isAssigned():					
		print("Device assigned - ver 1.54")
		print(device.getName())
		print(f"Port Number: {device.getPortNumber()}")
	else:
		print("Not assigned - ver 1.54")

def  OnMidiMsg(event):
	"""Function called on every midi message sent by controller"""
	process = Process(event)



			
