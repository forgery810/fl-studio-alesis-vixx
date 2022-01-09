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
import data
from data import button, mode, parameters, knob, colors, mixer_choice, scales
from midi import *
import _random
import config



current_channel = channels.selectedChannel()
current_track = mixer.trackNumber()

offset = [0, 16, 32, 48]


class Switch():

	root_note = 0 
	scale_choice = 0 
	lower_limit = 0 													# set in turning.py
	upper_limit = 0
	param_enter = True
	parameter = 0
	mode_toggle = 0	
	mixer_focused = ui.getFocused(midi.widMixer)
	channels_focused = ui.getFocused(midi.widChannelRack)
	browser_focused = ui.getFocused(midi.widBrowser)
	piano_focused = ui.getFocused(midi.widPianoRoll)
	nothing_focused = 1
	in_focus = [channels_focused, mixer_focused, browser_focused, piano_focused, nothing_focused]
	focused = in_focus.index(1)	
	offset_iter = 0	
	color_num = 0
	pitch_num = 0
	mixer_num = 0
	scale = 0
	note = 0
	shift_status = False
	pattern_length = patterns.getPatternLength(patterns.patternNumber())


	def switch_toggle(event):


		if event.data1 == button["record"]:			# This section is for buttons with leds that toggle on/off
				print('Record')
				transport.record()
				event.handled = True
	
		elif event.data1 == button["set_metronome"]:
			print('Set Metronome')
			transport.globalTransport(midi.FPT_Metronome, 110)
			event.handled = True

		elif event.data1 == button["overdub"]:
				print('Toggle Overdub Mode')
				transport.globalTransport(midi.FPT_Overdub, 112)
				event.handled = True

		elif event.data1 == button["loop"]:						
			print('Toggle Loop Mode')
			transport.globalTransport(midi.FPT_LoopRecord, 113)
			event.handled = True

		elif event.data1 == button["shift"]:
			print('Shift')
			if Switch.shift_status == False:
				Switch.shift_status = True
				ui.setHintMsg('Shift Active')
			elif Switch.shift_status == True:
				Switch.shift_status = False
				ui.setHintMsg('Shift Disabled')




	def switch_moment(event):
		if event.data1 == button["pad_mode_toggle"]:				# This Rotates through pad modes - standard, step sequencer, pad to channel		
			Switch.mode_toggle += 1
			if Switch.mode_toggle == 4:
				Switch.mode_toggle = 0
			print('Pad Mode: ' + mode[Switch.mode_toggle])
			ui.setHintMsg(mode[Switch.mode_toggle])

		elif event.midiId == 224: 								# pitch wheel
			Switch.pitch_num = event.data2	
			if Switch.shift_status == True:
				print(data.notes_list[int(mapvalues(Switch.pitch_num, 0, 11, 0, 244))])

		
																# Transport controls
		
		elif event.data1 == button["play"]:			
			transport.start()
			event.handled = True

		elif event.data1 == button["offset_range"]:
			Switch.offset_iter += 1
			if Switch.offset_iter == 2:     								# 2 here will limit to 32 steps, knobs. Changing to 4 will allow up to 64 steps, knobs. 
				Switch.offset_iter = 0
			ui.setHintMsg("Offset Range: " + str(Switch.offset_iter))
	
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



																	# Set mod wheel to control channels when channels focused and tracks when mixer
		elif event.data1 == button["mod_wheel"]:					
			if ui.getFocused(0):
				mixer.setTrackNumber(int(mapvalues(event.data2, 0, 64, 0, 127)))
				ui.scrollWindow(midi.widMixer, mixer.trackNumber())

			elif ui.getFocused(1):
				print("Channel Number: " + str(channels.selectedChannel()))
				channels.selectOneChannel(int(round(mapvalues(event.data2, channels.channelCount()-1, 0, 0, 127), 0)))				

		elif event.data1 == 72:
			print(channels.getChannelColor(channels.selectedChannel())) 
			Switch.color_num += 1
			if Switch.color_num == len(colors):
				Switch.color_num = 0
			if ui.getFocused(1):
				channels.setChannelColor(channels.selectedChannel(), colors[Switch.color_num])
			elif ui.getFocused(0):
				mixer.setTrackColor(mixer.trackNumber(), colors[Switch.color_num])
			event.handled = True
		
		elif event.data1 == button["enter"]:
			if ui.getFocused(4):
				print("Select Browser Item")
				ui.selectBrowserMenuItem()		
				event.handled = True
			elif ui.getFocused(1):
				print("Mute Channel")
				channels.muteChannel(channels.selectedChannel())
			elif ui.getFocused(0):
				print("Mute Track")
				mixer.muteTrack(mixer.trackNumber())
			else:
				print('enter')
				ui.enter()
				event.handled = True


		elif event.data1 in range(59, 64) and config.PATTERN_JUMP_ON:						# Sets jump to pattern
			patterns.jumpToPattern(event.data1 - 58)
			event.handled = True		

		elif event.data1 in range(75, 80) and config.PATTERN_JUMP_ON:
			patterns.jumpToPattern(event.data1 - 69)
			event.handled = True

		elif event.data1 == button["solo"]:
			print('Solo')
			if ui.getFocused(0):
				mixer.soloTrack(current_track)
			elif ui.getFocused(1):
				channels.soloChannel(channels.selectedChannel())

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
			
			if ui.getFocused(1) and Switch.mode_toggle == 1:
				print('Toggle Step Parameter')
				Switch.parameter += 1
				if Switch.parameter == 7:
					Switch.parameter = 0
				print(Switch.parameter)
				ui.setHintMsg(parameters[Switch.parameter])

			elif ui.getFocused(0):
				Switch.mixer_num += 1
				if Switch.mixer_num == 2:
					Switch.mixer_num = 0
				print('Mixer Mode: ' + str(Switch.mixer_num))
				ui.setHintMsg(mixer_choice[Switch.mixer_num])
			event.handled = True

		elif event.data1 == button["open_channel_sampler"]:			
			print('Open Sampler Channel')
			channels.showCSForm(channels.channelNumber(), -1)
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
			if Switch.shift_status == False:
				if ui.getFocused(4):
					ui.hideWindow(4)
					event.handled = True
				else:
					ui.showWindow(4)
					ui.setFocused(4)
					event.handled = True
			
					
		elif event.data1 == button["step_rec"]:	
			if ui.getFocused(0):
				mixer.armTrack(mixer.trackNumber())	
				print("Toggle Track Rec")

			else:			
				transport.globalTransport(midi.FPT_StepEdit, 114)
				print('Step Record')
				event.handled = True							

		elif event.data1 == button["quantize"]:
			print('quantize')
			channels.quickQuantize(channels.channelNumber())
			event.handled = True

		elif event.data1 == button["link_chan"]:
			print('link channel')
			mixer.linkTrackToChannel(0)

		elif event.data1 == button["rand_steps"]:
			print("Random")
			print(f'Pitch Bend: {event.pitchBend}')
			for i in range(patterns.getPatternLength(patterns.patternNumber())):
				channels.setGridBit(channels.channelNumber(), i, 0)
			for z in range (patterns.getPatternLength(patterns.patternNumber())):
				y = num_gen()
				if y > ( Switch.pitch_num * 516):
					channels.setGridBit(channels.channelNumber(), z, 1)
				else:
					pass
			event.handled = True

		elif event.data1 == button["rand_notes"]:
			print("Randomize Notes")
			Switch.note_gen()
			event.handled = True

	def note_gen():

		for i in range(patterns.getPatternLength(patterns.patternNumber())):
			note = scales[Switch.scale_choice][Switch.root_note][int(mapvalues(num_gen(), 0 + Switch.lower_limit, len(scales[Switch.scale_choice][Switch.root_note]) - Switch.upper_limit, 0, 65535))]
			# note = scales[0][0][int(mapvalues(num_gen(), 0, len(scales[0][0])-40, 0, 65535))]
			print(note)
			channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, note, 1)
			#channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, int(mapvalues(num_gen(), 48 , 96, 0, 65535)), 1)

	def mapvalues(value, tomin, tomax, frommin, frommax):
		input_value = value
		solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
		if  -0.01 < solution < 0.01:
			solution = 0
	#	print(f"Solution: {solution}")
		return solution

def num_gen():
	# print('num_gen')
	rand_obj = _random.Random()
	rand_obj.seed()
	rand_int = rand_obj.getrandbits(16) 
	return rand_int 


def mapvalues(value, tomin, tomax, frommin, frommax):
	input_value = value
	solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
	if  -0.01 < solution < 0.01:
		solution = 0
#	print(f"Solution: {solution}")
	return solution

