# name=Alesis VIxx-1.00
# Author: ts-forgery
# Version 1.00

#This program was designed using an Alesis VI61. It should work on the VI25 and VI49 as all buttons used have 
#the same MIDI CC number attached based on their position starting from the left of each row. The standard mapping 
#of CC numbers is used but I advise users to change all buttons to from CC Toggle to CC Momentary otherwise you will 
#have to press buttons twice.

# version 0.5
#
# eliminate button/sustain conflict while preserving sustain
# changed pattern control to arrow buttons in transport control section of keyboard
# eliminated new pattern button 
# mod wheel controls track and channel selection
# added focused dependent controls including mixer volume, panning control
# mixer track mute option
# added value pick-up knobs so knob must match value before it is engaged
# added pad modes - step sequencer and channel control
# added per step value controls for pitch, mod x , mod y  

import arrangement
import transport
import midi
import ui
import channels
import plugins
import mixer
import device
import patterns
from data import button, mode, parameters, knob, plugin_names
from midi import *

if device.isAssigned():					# check if device assigned. not currently used
	print("Device assigned - ver 1.00")
	print(device.getName())
	print(device.getPortNumber())

else:
	print("Not assigned - ver 1.00")

mixer_num = 0 				# for toggling mixer modes
proceed = False        			# stores bool value to decide if knob can change values
mode_toggle = 0				# for toggling pad mode
parameter = 0 				# step sequencer parameters
offset_iter = 0

def  OnMidiMsg(event):

	global proceed
	global tempChan
	global mode_toggle
	global parameter
	global offset
	global offset_iter
	global mixer_num

	current_pattern = patterns.patternNumber()
	current_channel = channels.channelNumber()

	mixer_focused = ui.getFocused(midi.widMixer)
	channels_focused = ui.getFocused(midi.widChannelRack)
	browser_focused = ui.getFocused(midi.widBrowser)
	piano_focused = ui.getFocused(midi.widPianoRoll)

	nothing_focused = 1
	mixer_choice = ['Volume', 'Panning'] 		
	in_focus = [channels_focused, mixer_focused, browser_focused, piano_focused, nothing_focused]
	focused = in_focus.index(1)
	event.handled = False
	offset = [0, 16, 32, 48]
	print(event.midiId, event.data1, event.data2, event.midiChan)


																												# Set to Pad per Channel
	if event.midiId == 144 and 60 <= event.data1 < channels.channelCount() + 60 and mode_toggle == 2:			
		print("pad")																							# == 144 only allows notes, not buttons
		PlayChannel(event.data1, event.data2)
		event.handled = True
																									# Set to Step Sequencer   and sets step (gridbit)
																									# .count() == .count(1) prevents setting steps in groups
																									

	if event.midiId == 144 and mode_toggle == 1 and channels.channelCount() == channels.channelCount(1):						
		if channels.getGridBit(channels.channelNumber(), event.data1 - 60 + offset[offset_iter]) == 0:						
			channels.setGridBit(channels.channelNumber(), event.data1 - 60 + offset[offset_iter], 1)	
			event.handled = True
																					
		else:															
			channels.setGridBit(channels.getChannelIndex(channels.selectedChannel(0, 3, 1)), event.data1 - 60 + offset[offset_iter], 0)     
			event.handled = True	

	if event.midiId == midi.MIDI_CONTROLCHANGE:

		if event.data2 > 0:
			
			if event.data1 in knob.values():
				print(ui.getFocusedPluginName())
				knobbb = Knob(event.data1, event.data2, focused)

				if channels_focused and mode_toggle == 1 and event.data1 in knob.values(): 
					print("adjusting step parameter") 
					knobbb.step_param(current_pattern, parameter)
					event.handled = True

				elif ui.getFocused(5):
					knobbb.plugin_control()

				else:
					knobbb.knob_turn()

			elif event.data1 == button["pad_mode_toggle"]:				# This Rotates through pad modes - standard, step sequencer, pad to channel		
				mode_toggle += 1
				if mode_toggle == 3:
					mode_toggle = 0
				print('Pad Mode: ' + mode[mode_toggle])
				ui.setHintMsg(mode[mode_toggle])

																		# Transport controls
			elif event.data1 == button["play"]:			
				transport.start()
				event.handled = True

			elif event.data1 == button["offset_range"]:
				offset_iter += 1
				if offset_iter == 4:
					offset_iter = 0
				ui.setHintMsg("Offset Range: " + str(offset_iter))
		
			elif event.data1 == button["stop"]:
				print('Stop')
				transport.stop()
				event.handled = True						
																		
			elif event.data1 == button["record"]:			
				print('Record')
				transport.record()
				event.handled = True

			elif event.data1 == button["pattern_down"]:
				if ui.getFocused(5):
					print("Previous Preset")
					ui.previous()

				else:
					print('Pattern Down')
					transport.globalTransport(midi.FPT_PatternJog, -1)
					event.handled = True
						
			elif event.data1 == button["pattern_up"]:
				if ui.getFocused(5):
					print("Next Preset")
					ui.next()

				else:
					print('Pattern Up')
					transport.globalTransport(midi.FPT_PatternJog, 1)
					event.handled = True

			elif event.data1 == button["loop"]:						
				print('Toggle Loop Record Mode')
				transport.globalTransport(midi.FPT_LoopRecord, 113)
				event.handled = True

			elif event.data1 == button["overdub"]:					
				print('Toggle Overdub Mode')
				transport.globalTransport(midi.FPT_Overdub, 112)
				event.handled = True
																		# Set mod wheel to control channels when channels focused and tracks when mixer
			elif event.data1 == button["mod_wheel"]:					
				if mixer_focused:
					mixer.setTrackNumber(int(mapvalues(event.data2, 0, 64, 0, 127)))

				elif channels_focused:
					print("Channel Number: " + str(current_channel))
					channels.selectOneChannel(int(round(mapvalues(event.data2, channels.channelCount()-1, 0, 0, 127), 0)))				

			elif event.data1 == button["solo"]:
				if mixer_focused:
					mixer.soloTrack(mixer.trackNumber())
				elif channels_focused:
					channels.soloChannel(channels.channelNumber())
				event.handled = True
			
			elif event.data1 == button["enter"]:
				if browser_focused:
					print("Select Browser Item")
					ui.selectBrowserMenuItem()		
					event.handled = True
				elif channels_focused:
					print("Mute Channel")
					channels.muteChannel(current_channel)
				elif mixer_focused:
					print("Mute Track")
					mixer.muteTrack(mixer.trackNumber())
				else:
					print('enter')
					ui.enter()
					event.handled = True

			elif event.data1 == button["view_plugin_picker"]:
				print('View Plugin Picker')
				transport.globalTransport(midi.FPT_F8, 67)
				event.handled = True	
				
			elif event.data1 == button["song_mode_toggle"]:			
				print('Toggle Song and Pattern Mode')
				transport.setLoopMode()
				event.handled = True
				
			elif event.data1 == button["view_playlist"]:			
				print('View Playlist')
				transport.globalTransport(midi.FPT_F5, 65)
				event.handled = True
				
			elif event.data1 == button["view_piano_roll"]:
				print('View Piano Roll')
				transport.globalTransport(midi.FPT_F7, 66)
				event.handled = True
			
			elif event.data1 == button["view_channel_rack"]:
				print('View Channel Rack')
				transport.globalTransport(midi.FPT_F6, 65)
				event.handled = True
				
			elif event.data1 == button["view_mixer"]:
				print('View Mixer')
				transport.globalTransport(midi.FPT_F9, 68)
				event.handled = True
																		# Toggle through step parameter options - pitch, pan etc. No Shift control right now. 
			elif event.data1 == button["step_parameter"]:
				
				if channels_focused and mode_toggle == 1:
					print('Toggle Step Parameter')
					parameter += 1
					if parameter == 7:
						parameter = 0
					print(parameter)
					ui.setHintMsg(parameters[parameter])

				elif mixer_focused:
					mixer_num += 1
					if mixer_num == 2:
						mixer_num = 0
					print('Mixer Mode: ' + str(mixer_num))
					ui.setHintMsg(mixer_choice[mixer_num])
				event.handled = True

			elif event.data1 == button["open_channel_sampler"]:			
				print('Open Sampler Channel')
				channels.showCSForm(channels.channelNumber(1))
				event.handled = True					
								
			elif event.data1 == button["left"]:							
				print('Left')
				ui.left()
				event.handled = True	
			
			elif event.data1 == button["down"]:							
				print('Down')
				ui.down()
				event.handled = True				
				
			elif event.data1 == button["right"]:						
				print('Right')
				ui.right()
				event.handled = True			

			elif event.data1 == button["save"]:
				print('Save')
				transport.globalTransport(midi.FPT_Save, 92)
																		# If mixer is open and mute mode selected, top row will mute respective track 

			elif event.data1 == button["undo"]:					
					print('Undo')
					transport.globalTransport(midi.FPT_Undo, 20)
					device.midiOutMsg(144, 1, 63, 80)
					event.handled = True

			elif event.data1 == button["set_metronome"]:	
					print('Set Metronome')
					transport.globalTransport(midi.FPT_Metronome, 110)
					event.handled = True

			elif event.data1 == button["escape"]:
				print('Escape')
				ui.escape()
				event.handled = True
			
			elif event.data1 == button["up"]:
				print('Up')
				ui.up()
				event.handled = True			

			elif event.data1 == button["rotate_window"]:				
				print('Rotate Window')
				ui.nextWindow()
				event.handled = True

			elif event.data1 == button["browser"]:				
				print('Browser')
				if ui.getFocused(4):
					ui.hideWindow(4)
					event.handled = True
				else:
					ui.showWindow(4)
					ui.setFocused(4)
					event.handled = True
					
			elif event.data1 == button["step_rec"]:	
				if mixer_focused:
					mixer.armTrack(mixer.trackNumber())	
					print("Toggle Track Rec")

				else:			
					print('Step Editor')
					transport.globalTransport(midi.FPT_StepEdit, 114)
					event.handled = True							


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
			elif self.focused == 0:
				channels.setChannelVolume(self.data_one-20, mapvalues(self.data_two, 0, 1, 0, 127))

		elif proceed == True and temp_chan != self.data_one - 19:
			print("proceed no more")
			proceed = False		

	def step_param(self, pat, param):

		self.pattern = pat
		self.parameter = param
		print(f"Parameter:  {self.parameter}")
		print(f"Data One:  {self.data_one}")
		print(f"Pattern:  {self.pattern}")
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


def PlayChannel(note, vel):												
	channels.selectOneChannel(note-60)
	channels.midiNoteOn(note-60, 60, vel)
	
def mapvalues(value, tomin, tomax, frommin, frommax):
	input_value = value
	solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
	if  -0.01 < solution < 0.01:
		solution = 0
	print(f"Solution: {solution}")
	return solution

	# mappedValue = minTo + (maxTo - minTo) * ((value - minFrom) / (maxFrom - minFrom));


		

			