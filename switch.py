import transport
from action import Action
from data import tr_buttons, mapping2
from config_layout import buttons

class Switch():

	def switch(event):

		if event.data1 in mapping2.keys():
			Action.call_func(buttons[mapping2[event.data1]])
			event.handled = True

	def transport(event):

		if event.data1 == tr_buttons["play"]:
			transport.start()
			event.handled = True

		elif event.data1 == tr_buttons["stop"]:
			transport.stop()
			event.handled = True

		elif event.data1 == tr_buttons["record"]:
			transport.record()
	
	
