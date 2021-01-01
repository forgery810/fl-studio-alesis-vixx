# name=Alesis VIxx                     
# Author: ts-forgery
# Version 0.1

#This program was designed using an Alesis VI61. It should work on the VI25 and VI49 as all switches used have 
#the same MIDI CC number attached based on their position starting from the left of each row. The standard mapping 
#of CC numbers is used but I advise users to change all switches to from CC Toggle to CC Momentary otherwise you will 
#have to press switches twice.

import transport
import midi
import ui
import channels
import mixer
import device

switch = {
    #Transport control switches				
	"record": 114,
	"loop": 115,
	"backward": 116,
	"forward": 117,
	"stop": 118,
	"play": 119,	
	#First row of switches 
	"undo": 48,							
	"set_metronome": 49,
	"escape": 50,
	"up": 51,
	"rotate_window": 52,
	"pattern_down": 53,	
	"pattern_up": 54,
	"new_pattern": 64,					
	#Second row of switches 
	"enter": 65,
	"left": 66,
	"down": 67,
	"right": 68,
	"open_channel_plugin": 69,
	"open_channel_sampler": 70,
	"song_mode_toggle": 80,
	#Third row of switches				
	"overdub": 81,
	"view_playlist": 82,
	"view_piano_roll": 83,
	"view_channel_rack": 84,
	"view_mixer": 85,
	"view_plugin_picker": 86,
	"event_editor": 87,
}

knob = {
	"knob_one": 20,
	"knob_two": 21,
	"knob_three": 22,
	"knob_four": 23,
	"knob_five": 24,
	"knob_six": 25,
	"knob_seven": 26,
	"knob_eight": 27,
	"knob_nine": 28,
}

def  OnMidiMsg(event):
	event.handled = False
	print(event.midiId, event.data1, event.data2)
	if event.midiId == midi.MIDI_CONTROLCHANGE: 
		if event.data2 > 0:
			
			if event.data1 == switch["play"]:			
				print('Play')
				transport.start()
				event.handled = True
				
			elif event.data1 == switch["stop"]:
				print('Stop')
				transport.stop()
				event.handled = True
				
			elif event.data1 == switch["record"]:			
				print('Record')
				transport.record()
				event.handled = True
				
			elif event.data1 == switch["forward"]:			
				print('Next')
				ui.next()
				event.handled = True
				
			elif event.data1 == switch["backward"]:			
				print('Previous')
				ui.previous()
				event.handled = True
				
			elif event.data1 == switch["enter"]:			
				print('enter')
				ui.enter()
				event.handled = True
				
			elif event.data1 == switch["new_pattern"]:		
				print('Open New Pattern')
				transport.globalTransport(midi.FPT_F4, 63)
				event.handled = True
				
			elif event.data1 == switch["set_metronome"]:
				print('Set Metronome')
				transport.globalTransport(midi.FPT_Metronome, 110)
				event.handled = True
						
			elif event.data1 == switch["loop"]:						
				print('Toggle Loop Record Mode')
				transport.globalTransport(midi.FPT_LoopRecord, 113)
				event.handled = True
				
			elif event.data1 == switch["song_mode_toggle"]:			
				print('Toggle Song and Pattern Mode')
				transport.setLoopMode()
				event.handled = True
				
			elif event.data1 == switch["overdub"]:					
				print('Toggle Overdub Mode')
				transport.globalTransport(midi.FPT_Overdub, 112)
				event.handled = True
				
			elif event.data1 == switch["view_playlist"]:			
				print('View Playlist')
				transport.globalTransport(midi.FPT_F5, 65)
				event.handled = True
				
			elif event.data1 == switch["view_piano_roll"]:
				print('View Piano Roll')
				transport.globalTransport(midi.FPT_F7, 66)
				event.handled = True
			
			elif event.data1 == switch["view_channel_rack"]:
				print('View Channel Rack')
				transport.globalTransport(midi.FPT_F6, 65)
				event.handled = True
				
			elif event.data1 == switch["view_mixer"]:
				print('View Mixer')
				transport.globalTransport(midi.FPT_F9, 68)
				event.handled = True
				
			elif event.data1 == switch["view_plugin_picker"]:
				print('View Plugin Picker')
				transport.globalTransport(midi.FPT_F8, 67)
				event.handled = True		
			
			elif event.data1 == switch["undo"]:							
				print('Undo')
				transport.globalTransport(midi.FPT_Undo, 20)
				event.handled = True
		
		#This controls the volume of the selected channel in the channel settings and
		#not in the mixer. Put a # before the next four lines if you wish to disable this. 		
			elif event.data1 == knob["knob_one"]:						
				print('Channel Volume')
				channels.setChannelVolume(channels.channelNumber(1), event.data2 / 127)
				event.handled = True

			elif event.data1 == switch["open_channel_plugin"]:							
				print('Open Plugin Channel')
				channels.showEditor(channels.channelNumber(1))
				event.handled = True				
				
			elif event.data1 == switch["open_channel_sampler"]:			
				print('Open Sampler Channel')
				channels.showCSForm(channels.channelNumber(1))
				event.handled = True				
			
			elif event.data1 == switch["rotate_window"]:				
				print('Rotate Window')
				ui.nextWindow()
				event.handled = True
								
			elif event.data1 == switch["left"]:							
				print('Left')
				ui.left()
				event.handled = True	
			
			elif event.data1 == switch["down"]:							
				print('Down')
				ui.down()
				event.handled = True				
				
			elif event.data1 == switch["right"]:						
				print('Right')
				ui.right()
				event.handled = True				
			
			elif event.data1 == switch["up"]:
				print('Up')
				ui.up()
				event.handled = True				
				
			elif event.data1 == switch["escape"]:
				print('Escape')
				ui.escape()
				event.handled = True
			
			elif event.data1 == switch["pattern_down"]:
				print('Pattern Down')
				transport.globalTransport(midi.FPT_PatternJog, -1)
				event.handled = True
				
			elif event.data1 == switch["pattern_up"]:
				print('Pattern Up')
				transport.globalTransport(midi.FPT_PatternJog, 1)
				event.handled = True
