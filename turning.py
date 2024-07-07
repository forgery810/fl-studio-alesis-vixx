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
from data import button,  knob
from midi import *
import switch
from switch import Switch
from notes import Scales, Notes
import notes
from plugindata import knob_num, transistor_bass, drumpad, dx10, plugin_dict
import data 
from action import Action
from pads import Pads 
from utility import Utility
from config import Config
from timing import Timing

class Knob:
	proceed = False
	temp_chan = 0
	get_track_value = 0	

	def __init__(self, event):
		self.event = event
		self.pad_offset = 60
		self.knob_offset = 51
		self.track_offset = 50
		self.round_margin = 0.10
		self.chan_in_grp = channels.selectedChannel()
		self.channel = channels.channelNumber()
		self.data_one = event.data1 
		self.data_two = event.data2
		self.two_rounded = round(self.data_two/127, 2)
		self.selected_channel = self.data_one - self.knob_offset + Pads.get_offset()
		self.selected_track = self.data_one - self.track_offset + Pads.get_offset()		

		self.triage()

	def triage(self):
		"""Function takes context of knob turn, if in step parameter editing mode or a plugin is focused, and sends data to correct function.
			Else if the mixer or channel rack is focused, function stores current value of channel/track/panner to allow for pickup""" 

		if ui.getFocused(1):
				if Action.get_shift_status(): 											# If channels focused and shift true, enter scale setting mode
					self.set_scale()			
				elif Pads.get_pad_mode() == 1 or Pads.get_pad_mode() == 3:
					self.step_param()
				elif Action.get_alt_status() == True: 
					self.selected()
					self.event.handled = True 
				elif Action.get_alt_status() == False:			
					self.get_match()													# If pad_mode standard or pad per channel knob changes channel volume

		elif ui.getFocused(5) and plugins.isValid(self.channel):					# If valid plugin focused, alter plugin.
			self.plugin_control()

		elif Action.get_alt_status() == True: 
			if Action.get_shift_status() == False:
				self.selected()
				self.event.handled = False

		elif Knob.proceed == True and Knob.temp_chan == self.data_one:
			self.knob_turn()

		elif Knob.proceed == True and Knob.temp_chan != self.data_one:		# Current knob does not matched stored knob 
			Knob.proceed = False		

		else:
			self.get_match()
			self.event.handled = True

	def get_match(self):
		if ui.getFocused(1) and self.selected_track < channels.channelCount():		# Get channel vol if Channels focused and valid channel
			if Pads.get_mixer_param_index() == 0:	
				Knob.get_track_value = channels.getChannelVolume(self.selected_channel) 
				self.check_if_matching()
			elif Pads.get_mixer_param_index() == 1:
				Knob.get_track_value = channels.getChannelPan(self.selected_channel)
				self.two_rounded = Utility.mapvalues(self.data_two, -1.0, 1.0, 0, 127)
				self.check_if_matching()

		elif ui.getFocused(0) and Knob.proceed == False:									# If mixer focused, store the current value at the destination of the knob
			if Pads.get_mixer_param_index() == 0:									# If level selected, store value
				Knob.get_track_value = mixer.getTrackVolume(self.selected_track) 

			elif Pads.get_mixer_param_index() == 1:									# If panning selected, store current value.
				# print('panning selected')
				Knob.get_track_value = mixer.getTrackPan(self.selected_track)
				self.two_rounded = Utility.mapvalues(self.data_two, -1.0, 1.0, 0, 127)
			self.check_if_matching()

	def check_if_matching(self):											
		# Knob must match current value before it engages.

		if self.two_rounded <= (Knob.get_track_value + self.round_margin) and self.two_rounded >= (Knob.get_track_value - self.round_margin):
			Knob.proceed = True
			Knob.temp_chan = self.data_one
			if Pads.get_pad_mode() != 1 and Pads.get_pad_mode() != 3:
				self.knob_turn()

		else:
			print('not matched')
			print(Knob.proceed)
			print(Knob.temp_chan)

	def knob_turn(self):
		"""Function changes level of selected channel/track once knob matches current value. Function exited when different knob used"""

		if Knob.proceed == True and Knob.temp_chan == self.data_one:
			if ui.getFocused(0):
				if Pads.get_mixer_param_index() == 0:
					mixer.setTrackVolume(self.selected_track, self.data_two/127)
				elif Pads.get_mixer_param_index() == 1:
					mixer.setTrackPan(self.selected_track, Utility.mapvalues(self.data_two, -1, 1, 0, 127))
				
			elif ui.getFocused(1) and self.selected_channel < channels.channelCount():
				if Pads.get_mixer_param_index() == 0:
					channels.setChannelVolume(self.selected_channel, Utility.mapvalues(self.data_two, 0, 1, 0, 127))
				elif Pads.get_mixer_param_index() == 1:
					channels.setChannelPan(self.selected_channel, Utility.mapvalues(self.data_two, -1, 1, 0, 127))

		elif Knob.proceed == True and Knob.temp_chan != self.data_one:		# Current knob does not matched stored knob 
			Knob.proceed = False		
			print('proceed false')

	def set_scale(self):
			"""If shift is active, first four knobs are used to set scale for random note generator"""

			if self.event.data1 == knob['knob_one']:
				Notes.set_root_note(self.data_two)
				Scales.display_scale()

			elif self.event.data1 == knob['knob_two']:
				Scales.set_scale(self.data_two)
				Scales.display_scale()

			elif self.event.data1 == knob['knob_three']:
				Notes.set_lower_limit(self.data_two)
				Notes.display_limits()

			elif self.event.data1 == knob['knob_four']:
				Notes.set_upper_limit(self.data_two)
				Notes.display_limits()

			self.event.handled = True		

	def step_param(self):

		step_pattern = 1
		param_entry = 3
		self.param_knob = self.data_one - self.knob_offset
		self.pattern = patterns.patternNumber()
		self.parameter = Pads.get_step_param()
		self.pad_step = Pads.get_last_press() - self.pad_offset
		self.step = 0

		if Pads.get_pad_mode() == param_entry and self.data_one < knob["knob_sixteen"] and ui.getFocused(1): 		# check if param entry mode is on and make sure knob is not out of parameter range
			channels.showGraphEditor(True, self.param_knob, self.pad_step - 60, self.channel)
																						# bool temporary, long param, long step, long index, (long globalIndex* = 1)			
			if self.param_knob == pModX or self.param_knob == pModY: 					#long index, long patNum, long step, long param, long value, (long globalIndex = 0)
				channels.setStepParameterByIndex(self.channel, self.pattern, self.pad_step, self.param_knob, int(Utility.mapvalues(self.data_two, 0 , 255, 0, 127)), 1)

			elif self.param_knob == pFinePitch:	
				channels.setStepParameterByIndex(self.channel, self.pattern, self.pad_step, self.param_knob, int(Utility.mapvalues(self.data_two, 0 , 240, 0, 127)), 1)

			else:
				channels.setStepParameterByIndex(self.channel, self.pattern, self.pad_step, self.param_knob, self.data_two, 1)

		if channels.getGridBit(channels.selectedChannel(), self.selected_channel) == 1 and Pads.get_pad_mode() == step_pattern and Action.get_shift_status() == False:
			channels.showGraphEditor(True, self.parameter, self.selected_channel, self.channel)

			if self.parameter == pModX or self.parameter == pModY:	
				channels.setStepParameterByIndex(channels.channelNumber(), self.pattern, self.selected_channel, self.parameter, int(Utility.mapvalues(self.data_two, 0 , 255, 0, 127)), 1)
			elif self.parameter == pFinePitch:	
				channels.setStepParameterByIndex(channels.channelNumber(), self.pattern, self.selected_channel, self.parameter, int(Utility.mapvalues(self.data_two, 0 , 240, 0, 127)), 1)			
			else:	
				channels.setStepParameterByIndex(channels.channelNumber(), self.pattern, self.selected_channel, self.parameter, self.data_two, 1)

	def plugin_control(self):
		
		plugin = plugins.getPluginName(self.channel)	
		self.param_count = plugins.getParamCount(self.channel)
		if plugin in plugin_dict:
			print('has plugin')			                                                                           																		
			plugins.setParamValue(Utility.mapvalues(self.data_two, 0, 1, 0, 127), plugin_dict[plugin][knob_num.index(self.data_one)], self.channel)
			self.event.handled = True
	
		else:		
			print('else')
			plugins.setParamValue(Utility.mapvalues(self.data_two, 0, 1, 0, 127), self.selected_track, self.channel)
			self.event.handled = True
			

	def selected(self):
		"""Function handles knob turns if alt active and channel/track levels altered only if selected"""

		if ui.getFocused(1):
			if self.data_one == knob["knob_one"]:
				channels.setChannelVolume(channels.selectedChannel(), Utility.mapvalues(self.data_two, 0, 1, 0, 127))
				self.event.handled = True
			elif self.data_one == knob["knob_two"]:
				channels.setChannelPan(channels.selectedChannel(), Utility.mapvalues(self.data_two, -1, 1, 0, 127))
				self.event.handled = True
			elif self.data_one == knob["knob_three"]:
				print('three')
				mixer.linkChannelToTrack(channels.selectedChannel(), int(Utility.mapvalues(self.data_two, 0, 125, 0, 127)))
				self.event.handled = True

		elif ui.getFocused(0):
			if self.data_one == knob["knob_one"]:
				mixer.setTrackVolume(mixer.trackNumber(), self.data_two/127, 1)
				self.event.handled = True
			elif self.data_one == knob["knob_two"]:
				mixer.setTrackPan(mixer.trackNumber(), Utility.mapvalues(self.data_two, -1, 1, 0, 127), 1)
				self.event.handled = True
			elif self.data_one == knob["knob_three"]:
				Action.set_mixer_route(int(Utility.mapvalues(self.data_two, 0, 125, 0, 127)))
				ui.setHintMsg(f"Route Current Track to Track {int(Utility.mapvalues(self.data_two, 0, 125, 0, 127))}")
				self.event.handled = True