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
import itertools
from midi import *
from config import Config 
from wheels import ModWheel, PitchWheel 
import _random 
from utility import Utility
from notes import Notes, Scales 
from pads import Pads 
from timing import Timing 

class Action():

	shift_status = False
	alter = ["Alter Selected Only", "Normal"]
	window_constants = ["mixer", "channels", "playlist", "piano", "browser"]
	color_num = 0
	parameter_index = 0
	mixer_num = 0
	mixer_send = 0 
	offset_iter = 0
	pitch_value = 0
	c = itertools.cycle(Config.COLORS)
	a = itertools.cycle(alter)
	alt_status = ''

	def call_func(f):
		method = getattr(Action, f)
		print(f)
		return method()

	def alt():
		Action.alt_status = next(Action.a) 
		Timing.begin_message(f'Alt Status: {Action.alt_status}')

	def set_mixer_route(track):
		Action.mixer_send = track 

	def get_mixer_route():
		return Action.mixer_send

	def mixer_route():
		mixer.setRouteTo(mixer.trackNumber(), Action.get_mixer_route(), 1)

	def get_alt_status():
		if Config.ALT_ALWAYS == True:
			return True 
		elif Action.alt_status == "Alter Selected Only":
			return True
		else:
			return False

	def pitch_wheel(event):
		PitchWheel.set_pitch_value(event)
		if Config.PITCH_BEND_ON and Action.shift_status == False and playlist.getPerformanceModeState() != 1:
			channels.setChannelPitch(channels.selectedChannel(), Utility.mapvalues(event.data2, -1, 1, 0, 127))
		elif Action.shift_status == True:
			print('shift_status')
			Action.pitch_value = event.data2	
			ui.setHintMsg(f'{(int(Utility.mapvalues(event.data2, 100, 0, 0, 128)))}%')

	def start():
		return transport.start()	

	def stop():
		return transport.stop()

	def setPosition(position = 0):
		return transport.setSongPos(position)

	def record():
		Utility.define_message('Record')
		return transport.record()

	def song_pat():
		return transport.setLoopMode()

	def step_rec():
		transport.globalTransport(midi.FPT_StepEdit, 114)		

	def overdub():
		return transport.globalTransport(midi.FPT_Overdub, 112)

	def metronome():
		return transport.globalTransport(midi.FPT_Metronome, 110)

	def loop_record():
		return transport.globalTransport(midi.FPT_LoopRecord, 113)

	def pattern_down():
		return transport.globalTransport(midi.FPT_PatternJog, -1)

	def pattern_up():
		return transport.globalTransport(midi.FPT_PatternJog, 1)

	def mute():
		if ui.getFocused(0):
			return mixer.muteTrack(mixer.trackNumber())
		elif ui.getFocused(1):
			return channels.muteChannel(channels.channelNumber())
		elif ui.getFocused(2):
			playlist.muteTrack(ModWheel.get_pl_mod_value())

	def open_channel():
		return channels.showCSForm(channels.channelNumber(), -1)

	def up():
		return ui.up()

	def down():
		return ui.down()

	def left():
		if ui.getFocused(5) and channels.getChannelType(channels.channelNumber()) != CT_Sampler:
			return ui.previous()
		elif ui.getFocused(widPlaylist):
			arrangement.jumpToMarker(0, 1)
		else:
			return ui.left()

	def right():
		if ui.getFocused(5) and channels.getChannelType(channels.channelNumber()) != CT_Sampler:
			return ui.next()
		elif ui.getFocused(widPlaylist):
			arrangement.jumpToMarker(1, 1)
		else:
			return ui.right()

	def enter():
		if ui.getFocused(4):
			ui.selectBrowserMenuItem()		
		elif ui.getFocused(widPlaylist):
			print('widp')
			print(arrangement.currentTime(1))
			arrangement.addAutoTimeMarker(arrangement.currentTime(1), str(arrangement.currentTime(1)))
		else:
			return ui.enter()

	def prev_pre_pat():
		if ui.getFocused(5) and channels.getChannelType(channels.channelNumber()) != CT_Sampler:
			return ui.previous()
		else:
			Action.pattern_down()

	def next_pre_pat():
		if ui.getFocused(5) and channels.getChannelType(channels.channelNumber()) != CT_Sampler:
			return ui.next()
		else:
			Action.pattern_up()		

	def b_down():
		ui.navigateBrowser(FPT_Down, 0)

	def b_right():
		ui.navigateBrowser(FPT_Right, 1)

	def b_left():
		ui.navigateBrowser(FPT_Left, 0)

	def b_select():
		ui.selectBrowserMenuItem()

	def undo():
		transport.globalTransport(midi.FPT_Undo, 20)
		device.midiOutMsg(144, 1, 63, 80)

	def focus_mixer():
		ui.showWindow(widMixer)

	def focus_channels():
		ui.showWindow(1)

	def focus_playlist():
		ui.showWindow(2)

	def focus_piano():
		ui.showWindow(3)

	def focus_browser():
		ui.showWindow(4)

	def open_plugins():
		transport.globalTransport(midi.FPT_F8, 67)

	def cut():
		ui.cut()

	def copy():		
		ui.copy()

	def copy_all():
		channels.selectAll()
		ui.copy()

	def paste():
		ui.paste()

	def insert():
		ui.insert()

	def delete():
		ui.delete()

	def next():
		ui.next()

	def previous():
		ui.previous()

	def escape():
		ui.escape()

	def next_preset():
		if plugins.isValid(channels.selectedChannel()):
			plugins.nextPreset(channels.selectedChannel())	

	def prev_preset():
		if plugins.isValid(channels.selectedChannel()):
			plugins.prevPreset(channels.selectedChannel())

	def arm_track():
		mixer.armTrack(mixer.trackNumber())

	def next():
		ui.next()

	def previous():
		ui.previous()

	def quantize():
		channels.quickQuantize(channels.channelNumber())

	def rotate():
		ui.nextWindow()

	def tap_tempo():
		transport.globalTransport(midi.FPT_TapTempo, 100)

	def wait_for_input():
		transport.globalTransport(midi.FPT_WaitForInput, 111)

	def item_menu():
		transport.globalTransport(midi.FPT_ItemMenu, 91)

	def menu():
		transport.globalTransport(midi.FPT_Menu, 90)

	def undo_up():
		transport.globalTransport(midi.FPT_UndoUp, 21)

	def countdown():
		transport.globalTransport(midi.FPT_CountDown, 115)
	
	def new_pattern():
		transport.globalTransport(midi.FPT_F4, 63)

	def save():
		transport.globalTransport(midi.FPT_Save, 92)

	def menu():
		transport.globalTransport(midi.FPT_Menu, 90)

	def snap_toggle():
		transport.globalTransport(midi.FPT_Snap, 48)

	def solo():
		if ui.getFocused(widMixer):
			mixer.soloTrack(mixer.trackNumber())
		elif ui.getFocused(widChannelRack):
			channels.soloChannel(channels.selectedChannel())
		elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(ModWheel.get_pl_mod_value()):
			playlist.soloTrack(ModWheel.get_pl_mod_value())

	def link_mix():
		mixer.linkTrackToChannel(0)

	def item_menu():
		transport.globalTransport(FPT_ItemMenu, 91)

	def countdown():
		transport.globalTransport(FPT_CountDown, 115)
		
	def change_color():
		if ui.getFocused(widChannelRack):
			channels.setChannelColor(channels.selectedChannel(),  next(Action.c))
		elif ui.getFocused(widMixer):
			mixer.setTrackColor(mixer.trackNumber(), next(Action.c))
		elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(ModWheel.get_pl_mod_value()):
			print(ModWheel.get_pl_mod_value())

			playlist.setTrackColor(ModWheel.get_pl_mod_value(), next(Action.c))

	def trig_clip():
		playlist.triggerLiveClip(1, 1, midi.TLC_MuteOthers | midi.TLC_Fill)
		print(playlist.getLiveStatus(1))

	def rand_pat():
			"""Function clears pattern and for each step, generates a random number. The number is checked"""
			
			for i in range(patterns.getPatternLength(patterns.patternNumber())):
				channels.setGridBit(channels.channelNumber(), i, 0)
			for z in range (patterns.getPatternLength(patterns.patternNumber())):
				y = Utility.num_gen()
				if y > ( PitchWheel.get_pitch_value() * 516):
					channels.setGridBit(channels.channelNumber(), z, 1)
				else:
					pass

	def rand_notes():
		"""function sets random notes for selected pattern when called based on scale/root selected in switch along with Knob() class"""

		scale = Scales.get_scale_choice()
		root = Notes.get_root_note()
		upper = Notes.get_upper_limit()
		lower = Notes.get_lower_limit()
		for i in range(patterns.getPatternLength(patterns.patternNumber())):
			note = Scales.scales[scale][int(Utility.mapvalues(Utility.num_gen(), lower, len(Scales.scales[scale]) + upper, 0, 65535))]
			# print(note)
			channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, note + root, 1)		

	def shift():
		if Action.shift_status == False:
			Action.shift_status = True
			Timing.begin_message('Shift Active')
		elif Action.shift_status == True:
			Action.shift_status = False
			Timing.begin_message('Shift Disabled')

	def get_shift_status():
		return Action.shift_status

	def pad_mode():
		return Pads.toggle_pad_mode()

	def toggle_offset():
		return Pads.toggle_offset()

	def step_param():
		Pads.toggle_step_param()

	def toggle_range():
		Pads.toggle_offset()

	def get_step_param():
		return Action.parameter_index

	def get_mixer_num():
		return Action.mixer_num

	def nothing():
		pass