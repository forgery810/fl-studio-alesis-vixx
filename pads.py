import midi
import ui
import channels
import playlist
import plugins
import device
from midi import *
from plugindata import *
from utility import Utility
from timing import Timing
from wheels import ModWheel, PitchWheel

offset = [0, 16, 32, 48]

class Pads():

	temp_step = [0]
	modes = ["Standard", "Step Pattern", "Pad per Channel", "Parameter Entry"]
	parameters = ["Pitch", "Velocity", "Release", "Fine Pitch", "Panning", "Mod x", "Mod y"]
	mixer_param = ["Level", "Panning"]
	mixer_param_index = 0 
	mode_index = 0
	offset_index = 0
	parameter_index = 0

	def toggle_offset():
		Pads.offset_index += 1
		if Pads.offset_index >= 2:
			Pads.offset_index = 0
		Timing.begin_message(f'Knob/Pad Range: +{offset[Pads.offset_index]}')
		# ui.setHintMsg(f'Knob/Pad Range: +{offset[Pads.offset_index]}')

	def get_offset():
		return offset[Pads.offset_index]

	def toggle_pad_mode():
		Pads.mode_index += 1
		if Pads.mode_index > 3:
			Pads.mode_index = 0
		print(f'Padmode: {Pads.get_mode_name()}')
		Timing.begin_message(f'Pad Mode: {Pads.get_mode_name()}')

	def get_pad_mode():
		return Pads.mode_index

	def get_mode_name():
		return Pads.modes[Pads.get_pad_mode()]

	def get_step_param():
		return Pads.parameter_index

	def get_last_press():
		return Pads.temp_step[0]

	def toggle_step_param():
		print(Pads.get_pad_mode())
		if ui.getFocused(1) and Pads.get_pad_mode() == 1:
				print('Toggle Step Parameter')
				Pads.parameter_index += 1
				if Pads.parameter_index == 7:
					Pads.parameter_index = 0
				print(Pads.parameter_index)
				Timing.begin_message(Pads.parameters[Pads.get_step_param()])

		elif ui.getFocused(0) or ui.getFocused(1):
			Pads.mixer_param_index += 1
			if Pads.mixer_param_index == 2:
				Pads.mixer_param_index = 0
			print('Mixer Mode: ' + str(Pads.mixer_param_index))
			Timing.begin_message(f'{Pads.mixer_param[Pads.mixer_param_index]}')		

	def get_mixer_param_index():
		return Pads.mixer_param_index

	def get_mixer_param_name():
		return Pads.mixer_param[Pads.get_mixer_param_index()]

	def pad_hit(event):

		if playlist.getPerformanceModeState() == 1 and ui.getFocused(widPlaylist):
			if PitchWheel.get_pitch_value() > 85:
				playlist.triggerLiveClip(ModWheel.get_pl_mod_value(), -1, TLC_Fill | TLC_MuteOthers)
				event.handled = True
			elif PitchWheel.get_pitch_value() < 15:
				playlist.triggerLiveClip(ModWheel.get_pl_mod_value(), event.data1 - 60, TLC_Fill | TLC_MuteOthers | TLC_Queue)
				event.handled = True
			else:
				playlist.triggerLiveClip(ModWheel.get_pl_mod_value(), event.data1 - 60, TLC_Fill | TLC_MuteOthers)
				event.handled = True				

		if event.midiId == 144:
			Pads.temp_step.clear()
			Pads.temp_step.append(event.data1 + Pads.get_offset())

		if ui.getFocused(5) and plugins.isValid(channels.selectedChannel()):
			if event.midiId == 128 and event.data2 != 0:
				print('skip')
			elif plugins.getPluginName(channels.selectedChannel()) == 'FPC' and event.data1 in alesis_pads:
				print('FPC')
				channels.midiNoteOn(channels.selectedChannel(), FPC_pads[alesis_pads.index(event.data1 + offset[Pads.get_pad_mode()])], event.data2)
				event.handled = True

		elif Pads.get_pad_mode() == 1 and event.midiId == 144:		
			print('setGridBit')				
			if channels.getGridBit(channels.selectedChannel(), event.data1 - 60 + Pads.get_offset()) == 0:						
				channels.setGridBit(channels.selectedChannel(), event.data1 - 60 + Pads.get_offset(), 1)	
				event.handled = True
			else:															
				channels.setGridBit(channels.selectedChannel(), event.data1 - 60 + Pads.get_offset(), 0)    
				event.handled = True	

		elif Pads.get_pad_mode() == 2  and 60 <= event.data1 < (channels.channelCount() + 60):
			channels.selectOneChannel(event.data1-60)  
			channels.midiNoteOn(event.data1-60, 60, event.data2)
			event.handled = True

