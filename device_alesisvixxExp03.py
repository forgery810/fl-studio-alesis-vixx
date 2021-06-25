# name=Alesis VIxx1betaInprogress3
# Author: ts-forgery
# Version 0.3

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


# to do:

# organize code into classes for better management
# change some buttons to toggle so light indicates on/off				
# match drum pads with FPC 
# change mixer track for channels in channel mode (might not be possible)
# auto-recongnize plugins for knob assigment
# replace map values

import arrangement
import transport
import midi
import ui
import channels
import plugins
import mixer
import device
import patterns
from data import button, mode, parameters, knob
from midi import *

if device.isAssigned():					# check if device assigned. not currently used
	print("Device assigned")
else:
	print("Not assigned")

mixer_num = 0 				# for toggling mixer modes
proceed = 0        			# stores bool value to decide if knob can change values
mode_toggle = 0				# for toggling pad mode
parameter = 0 				# step sequencer parameters


def  OnMidiMsg(event):

	global proceed
	global tempChan
	global mode_toggle
	global parameter
	global mixer_num
	
	current_pattern = patterns.patternNumber()
	current_channel = channels.channelNumber()
	mixer_focused = ui.getFocused(midi.widMixer)
	channels_focused = ui.getFocused(midi.widChannelRack)
	browser_focused = ui.getFocused(midi.widBrowser)
	mixer_choice = ['Volume', 'Mute', 'Panning', 'Record'] 		# mixer options. record not yet used

	event.handled = False
	print(event.midiId, event.data1, event.data2)

																												# Set to Pad per Channel
	if event.midiId == 144 and 60 <= event.data1 < channels.channelCount() + 60 and mode_toggle == 2:			
		print("pad")																							# == 144 only allows notes, not buttons
		PlayChannel(event.data1, event.data2)
		event.handled = True
																									# Set to Step Sequencer   and sets step (gridbit)
																									# .count() == .count(1) prevents setting steps in groups
																									

	if event.midiId == 144 and mode_toggle == 1 and channels.channelCount() == channels.channelCount(1):						
		if channels.getGridBit(channels.channelNumber(), event.data1 - 60) == 0:						
			channels.setGridBit(channels.channelNumber(), event.data1 - 60, 1)	
			event.handled = True
																					
		else:															
			channels.setGridBit(channels.getChannelIndex(channels.selectedChannel(0, 3, 1)), event.data1 - 60, 0)     
			event.handled = True	



	if event.midiId == midi.MIDI_CONTROLCHANGE:
		if event.data2 > 0:

			if event.data1 == button["pad_mode_toggle"]:				# This Rotates through pad modes - standard, step sequencer, pad to channel		
				mode_toggle += 1
				if mode_toggle == 3:
					mode_toggle = 0
				print('Pad Mode: ' + mode[mode_toggle])
				ui.setHintMsg(mode[mode_toggle])
																		# Transport controls
			elif event.data1 == button["play"]:			
				transport.start()
				event.handled = True
				
			elif event.data1 == button["stop"]:
				print('Stop')
				transport.stop()
				event.handled = True						
																		
			elif event.data1 == button["record"]:			
				print('Record')
				transport.record()
				event.handled = True

			elif event.data1 == button["pattern_down"]:
				print('Pattern Down')
				transport.globalTransport(midi.FPT_PatternJog, -1)
				event.handled = True
						
			elif event.data1 == button["pattern_up"]:
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
					mixer.setTrackNumber(int(mapvalues(event.data2, 0, 50, 0, 127)))

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
					ui.selectBrowserMenuItem()		
					event.handled = True

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
					if mixer_num == 3:
						mixer_num = 0
					print('Mixer Mode: ' + str(mixer_num))
					ui.setHintMsg(mixer_choice[mixer_num])
					
				event.handled = True		
																	# Controls knobs. Needs consolidation ####

																		# If panning mode active and knob turned

			if mixer_focused and mixer_num == 2 and event.data1 in knob.values():
				print("panning")

				print(round(mixer.getTrackPan(event.data1-19), 2))
				if round(mixer.getTrackPan(event.data1-19), 1) == round(mapvalues(event.data2, -1.0, 1.0, 0, 127), 1):		
					tempChan = event.data1-19
					print("Equal")
					proceed = True

				if proceed == True and tempChan == event.data1-19:
					mixer.setTrackPan(event.data1-19, mapvalues(event.data2, -1, 1, 0, 127))
					event.handled = True

				elif proceed == True and tempChan != event.data1 - 19:
					proceed = False		

			 															# # Same process for mixer as discussed for panning above
			 															# < 2 is so knobs only change volume in volume or mute modes

			if mixer_focused and mixer_num < 2 and event.data1 in knob.values():
																									
				if round(mixer.getTrackVolume(event.data1-19), 2) == round(event.data2/127, 2):
					tempChan = event.data1-19
					print("Equal")
					proceed = True
				
				if proceed == True and tempChan == event.data1-19:
					if mixer.trackNumber() == 0:
						mixer.setTrackVolume(event.data1-20, event.data2/127)
						event.handled = True
					else:
						mixer.setTrackVolume(event.data1-19, event.data2/127)
						event.handled = True

				elif proceed == True and tempChan != event.data1 - 19:
					proceed = False


			if channels_focused and mode_toggle == 1 and event.data1 in knob.values():  

				if channels.getGridBit(channels.channelNumber(), event.data1 - 20) == 1:
					if 6 <= parameter >= 5:
						channels.setStepParameterByIndex(current_channel, current_pattern, event.data1-20, parameter, int(mapvalues(event.data2, 0 , 255, 0, 127)), 1)

					elif parameter == 3:
						channels.setStepParameterByIndex(current_channel, current_pattern, event.data1-20, parameter, int(mapvalues(event.data2, 0 , 240, 0, 127)), 1)

					else:	

						channels.setStepParameterByIndex(channels.channelNumber(), patterns.patternNumber(), event.data1-20, parameter, event.data2, 1)

				print("Change Step Parameter: " + str(parameter))
				print("Channel Number: " + str(current_channel))
				print("Pattern Number:  "+ str(patterns.patternNumber()))
				event.handled = True
		






																						# Sets channel volume if channels are focused

			if channels_focused and mode_toggle != 1 and event.data1 in knob.values() and event.data1-20 < channels.channelCount():

				if round(channels.getChannelVolume(event.data1-20), 2) == round(mapvalues(event.data2, 0, 1, 0, 127), 2):		
					tempChan = event.data1-20
					print("Equal")
					proceed = True

				if proceed == True and tempChan == event.data1-20:
					channels.setChannelVolume(event.data1-20, mapvalues(event.data2, 0, 1, 0, 127))
					event.handled = True

				elif proceed == True and tempChan != event.data1 - 19:
					proceed = False		


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
																		# If mixer is open and mute mode selected, top row will mute respective track 
			elif event.data1 in range(48, 64):

				if mixer_num == 1 and mixer_focused:
					mixer.muteTrack(event.data1-47)
					print("muted")
					event.handled = True

				else:			
					if event.data1 == button["undo"]:					
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
						if ui.getFocused(widBrowser):
							ui.hideWindow(widBrowser)
							event.handled = True
						else:
							ui.showWindow(widBrowser)
							ui.setFocused(widBrowser)
							event.handled = True
							
					elif event.data1 == button["step_editor"]:					
						print('Step Editor')
						transport.globalTransport(midi.FPT_StepEdit, 114)
						event.handled = True							


def PlayChannel(note, vel):												
	channels.selectOneChannel(note-60)
	channels.midiNoteOn(note-60, 60, vel)
	



def mapvalues(value, tomin, tomax, frommin, frommax):
	input_value = value
	solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
	return solution

	# mappedValue = minTo + (maxTo - minTo) * ((value - minFrom) / (maxFrom - minFrom));


		

			