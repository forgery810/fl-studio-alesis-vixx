# assigns controls to knobs

import arrangement
import transport
import midi
import ui
import channels
import plugins
import mixer
import device
import patterns
from data import button, mode, parameters, knob, colors
from midi import *
import switch
from switch import Switch
import notes
from plugindata import knob_num, transistor_bass, drumpad, dx10, plugin_dict
import data 

offset = [0, 16, 32, 48]
temp_step = 0
# proceed = False

class Knob:
	global proceed

	def __init__(self, event):
		global proceed

		self.event = event
		global temp_chan
		proceed = False
		self.mode_toggle = Switch.mode_toggle
		# self.mixer_num = mixer.trackNumber()
		self.channel = channels.channelNumber()
		self.round_offset = 0.16
		self.get_track_value = 0
		self.data_one = event.data1 + offset[switch.Switch.offset_iter]
		self.data_two = event.data2
		self.two_rounded = round(self.data_two/127, 2)
		self.plugin = 0
		self.event_one = event.data1
		print('knob class')

		if ui.getFocused(1) and Switch.shift_status == True:
			print('enter step param edit in turning')
			if event.data1 == knob['knob_one']:
				Switch.root_note = int(mapvalues(self.data_two, 0, 11, 0, 127))
				ui.setHintMsg(data.notes_list [int(mapvalues(self.data_two, 0, 11, 0, 127)) ] )
				print(Switch.root_note)
				event.handled = True

			if event.data1 == knob['knob_two']:
				Switch.scale_choice = int(mapvalues(self.data_two, 0, len(data.scale_names)-1, 0, 127))
				ui.setHintMsg(data.scale_names[int(mapvalues(self.data_two, 0, len(data.scale_names)-1, 0, 127))])
				print(Switch.scale_choice)
				event.handled = True

			if event.data1 == knob['knob_three']:
				Switch.lower_limit = int(mapvalues(self.data_two, 0, 25, 0, 127))
				ui.setHintMsg("Setting Lower Limit")
				print(Switch.lower_limit)
				event.handled = True

			if event.data1 == knob['knob_four']:
				Switch.upper_limit = int(mapvalues(self.data_two, 50, 0, 0, 127))
				ui.setHintMsg("Setting Upper Limit")
				print(Switch.upper_limit)
				event.handled = True


		elif ui.getFocused(5) and plugins.isValid(self.channel):
			print('plugin control')
			self.plugin_control()


		elif ui.getFocused(0) and proceed == False:						# This stores the current value at the destination of the knob
			# print('proceed false mixer focused')
			if Switch.mixer_num == 0:
				# print('stored mixer')
				if mixer.trackNumber() == 0:								# Check if master is selected
					self.get_track_value = mixer.getTrackVolume(0)
					# print('master vol')
				else:		
					self.get_track_value = mixer.getTrackVolume(self.data_one - 19) 

			elif Switch.mixer_num == 1:
				# print('store panning info')
				self.get_track_value = mixer.getTrackPan(self.data_one-19)
				print(self.get_track_value)
				self.two_rounded = mapvalues(self.data_two, -1.0, 1.0, 0, 127)
				print(self.two_rounded)

		elif ui.getFocused(1) and Switch.shift_status == False:
			# print('stored channel')
			if self.mode_toggle != 1 and self.mode_toggle != 3:
				if self.data_one-20 < channels.channelCount():
					self.get_track_value = channels.getChannelVolume(self.data_one-20) 
			else:
				# print('go to step parameter function')
				self.step_param()


	
																					# Knob must match current value before it engages.
		if self.two_rounded <= (self.get_track_value + self.round_offset) and self.two_rounded >= (self.get_track_value - self.round_offset):
			print("matched") 
			proceed = True
			temp_chan = self.data_one
			# print(f'temp chan:  {temp_chan}')
			if switch.Switch.mode_toggle != 1 and Switch.mode_toggle != 3 or ui.getFocused(1)==False:
				# print('enter knob turn function')
				self.knob_turn()


	def knob_turn(self):
		global proceed
		# print('in knob turn function')

		if proceed == True and temp_chan == self.data_one:
			print("proceeding")
			if ui.getFocused(0) and Switch.mixer_num == 0:
				if mixer.trackNumber() == 0 and self.data_one == 20:
					mixer.setTrackVolume(0, self.data_two/127)
				else:
					# print('setting Track Volume')
					mixer.setTrackVolume(self.data_one-19, self.data_two/127)
			elif ui.getFocused(0) and Switch.mixer_num == 1:
				mixer.setTrackPan(self.data_one-19, mapvalues(self.data_two, -1, 1, 0, 127))
				# print(f'panning: {mapvalues(self.data_two, -1, 1, 0, 127)}')
			elif ui.getFocused(1) and self.data_one-20 < channels.channelCount()  and Switch.shift_status == False:
				# print(f'volume: {mapvalues(self.data_two, -1, 1, 0, 127)}')
				channels.setChannelVolume(self.data_one-20, mapvalues(self.data_two, 0, 1, 0, 127))
			# else:
			# 	print('leaving')	
		elif proceed == True and temp_chan != self.data_one:
			print("proceed no more")
			proceed = False		


	def step_param(self):

		self.pattern = patterns.patternNumber()
		self.parameter = switch.Switch.parameter
		self.pad_step = notes.temp_step[0]
		self.step = 0
		self.nothing = 0


		if Switch.mode_toggle == 3 and self.event_one < 27 and ui.getFocused(1): 		# check if param entry mode is on and make sure knob is not out of parameter range
			print('in param knob mode')
			ui.setHintMsg(parameters[self.event_one -20])
			if 6 <= self.event_one - 20 >= 5:
				channels.setStepParameterByIndex(self.channel, self.pattern, self.pad_step - 60, self.event_one - 20, int(mapvalues(self.data_two, 0 , 255, 0, 127)), 1)

			elif self.event_one - 20 == 3:
				channels.setStepParameterByIndex(self.channel, self.pattern, self.pad_step - 60, self.event_one - 20, int(mapvalues(self.data_two, 0 , 240, 0, 127)), 1)

			else:
				channels.setStepParameterByIndex(self.channel, self.pattern, self.pad_step - 60, self.event_one - 20, self.data_two, 1)


		if channels.getGridBit(channels.channelNumber(), self.data_one - 20) == 1 and Switch.mode_toggle == 1 and Switch.shift_status == False:
			# print(f'Switch Mode toggle: {Switch.mode_toggle}')
			print("getGridBit gotten")
			if 6 <= self.parameter >= 5:
				channels.setStepParameterByIndex(self.channel, self.pattern, self.data_one - 20, self.parameter, int(mapvalues(self.data_two, 0 , 255, 0, 127)), 1)

			elif self.parameter == 3:
				channels.setStepParameterByIndex(self.channel, self.pattern, self.data_one - 20, self.parameter, int(mapvalues(self.data_two, 0 , 240, 0, 127)), 1)
			
			else:	
				channels.setStepParameterByIndex(channels.channelNumber(), patterns.patternNumber(), self.data_one - 20, self.parameter, self.data_two, 1)
			
		# else:
		# 	print("getGridbit not gotten")


	def plugin_control(self):
		
		self.plugin = plugins.getPluginName(self.channel)	
		self.param_count = plugins.getParamCount(self.channel)

		if self.data_one < self.param_count + 19:				#this is probably unneccessary
			if self.plugin in plugin_dict:
				print('has plugin')			
				# print(plugin_dict[self.plugin][knob_num.index(self.data_one)])                                                                             																		
				plugins.setParamValue(mapvalues(self.data_two, 0, 1, 0, 127), plugin_dict[self.plugin][knob_num.index(self.data_one)], self.channel)
				return

			else:		
				print('else')
				plugins.setParamValue(mapvalues(self.data_two, 0, 1, 0, 127), self.data_one - 20, self.channel)
				return



def mapvalues(value, tomin, tomax, frommin, frommax):
	input_value = value
	solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
	if  -0.01 < solution < 0.01:
		solution = 0
#	print(f"Solution: {solution}")
	return solution