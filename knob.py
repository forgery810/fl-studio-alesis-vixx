import arrangement
import transport
import midi
import playlist
import ui
import channels
import plugins
import mixer
import device
import patterns
from data import button, mode, parameters, knob, colors
from midi import *

class Knob:

	def __init__(self, data_one, data_two, focused):

		global offset
		global offset_iter
		global proceed
		global temp_chan
		global mode_toggle
		global mixer_num
		self.channel = channels.channelNumber()
		self.round_offset = 0.1
		self.get_track = 0
		self.data_one = data_one + offset[offset_iter]
		self.data_two = data_two
		self.two_rounded = round(self.data_two/127, 2)
		self.focused = focused

		if self.focused == 1 and mixer_num == 0:
			self.get_track = mixer.getTrackVolume(self.data_one - 19) 
		elif self.focused == 0 and mode_toggle != 1:
			if self.data_one-20 < channels.channelCount():
				self.get_track = channels.getChannelVolume(self.data_one-20) 
		elif self.focused == 1 and mixer_num == 1:
			self.get_track = mixer.getTrackPan(self.data_one-19)
			self.two_rounded = mapvalues(self.data_two, -1.0, 1.0, 0, 127)
		print("Knob Class")
																					# Knob must match current value before it engages.
		if self.two_rounded <= self.get_track + self.round_offset and self.two_rounded >= self.get_track - self.round_offset:
			print("matched") 
			proceed = True
			temp_chan = self.data_one

	def knob_turn(self):
		global proceed

		if proceed == True and temp_chan == self.data_one:
			print("proceeding")
			if self.focused == 1 and mixer_num == 0:
				if mixer.trackNumber() == 0:
					mixer.setTrackVolume(0, self.data_two/127)
				else:
					mixer.setTrackVolume(self.data_one-19, self.data_two/127)
			elif self.focused == 1 and mixer_num == 1:
				mixer.setTrackPan(self.data_one-19, mapvalues(self.data_two, -1, 1, 0, 127))
			elif self.focused == 0 and self.data_one-20 < channels.channelCount():
				print("Channel Count")
				print(channels.channelCount())
				print("Active Channel")
				print(self.data_one-20)
				channels.setChannelVolume(self.data_one-20, mapvalues(self.data_two, 0, 1, 0, 127))

		elif proceed == True and temp_chan != self.data_one - 19:
			print("proceed no more")
			proceed = False		

	def step_param(self, pat, param):

		self.pattern = pat
		self.parameter = param
#		print(f"Parameter:  {self.parameter}")
#		print(f"Data One:  {self.data_one}")
#		print(f"Pattern:  {self.pattern}")
		if channels.getGridBit(channels.channelNumber(), self.data_one - 20) == 1:
			print("getGridBit gotten")
			if 6 <= self.parameter >= 5:
				channels.setStepParameterByIndex(self.channel, self.pattern, self.data_one - 20, self.parameter, int(mapvalues(self.data_two, 0 , 255, 0, 127)), 1)

			elif parameter == 3:
				channels.setStepParameterByIndex(self.channel, self.pattern, self.data_one - 20, self.parameter, int(mapvalues(self.data_two, 0 , 240, 0, 127)), 1)
			
			else:	
				channels.setStepParameterByIndex(channels.channelNumber(), patterns.patternNumber(), self.data_one - 20, self.parameter, self.data_two, 1)
			
		else:
			print("getGridbit not gotten")

	def plugin_control(self):
		print('mapped value')
		print(mapvalues(self.data_two, 0, 1, 0, 127))
		plugins.setParamValue(mapvalues(self.data_two, 0, 1, 0, 127), self.data_one - 20, self.channel)
		
def mapvalues(value, tomin, tomax, frommin, frommax):
	input_value = value
	solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
	if  -0.01 < solution < 0.01:
		solution = 0
#	print(f"Solution: {solution}")
	return solution