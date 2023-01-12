import ui
from midi import *
import mixer 
import channels 
import playlist
from utility import Utility
import midi
from config import Config

class ModWheel():
	mod_value = 0

	def process(event):
		ModWheel.set_mod_value(event)
		ModWheel.mod_scroll(event)

	def set_mod_value(event):
		ModWheel.mod_value = event.data2

	def get_mod_value():
		return ModWheel.mod_value

	def get_pl_mod_value():
		return int(Utility.mapvalues(ModWheel.get_mod_value(), Config.PLAYLIST_REACH, 1, 0, 127))

	def mod_scroll(event):
		if ui.getFocused(0):
			mixer.setTrackNumber(int(Utility.mapvalues(event.data2, 0, 64, 0, 127)))
			ui.scrollWindow(midi.widMixer, mixer.trackNumber())
		elif ui.getFocused(1):
			print("Channel Number: " + str(channels.selectedChannel()))
			channels.selectOneChannel(int(round(Utility.mapvalues(event.data2, channels.channelCount()-1, 0, 0, 127), 0)))			
		elif ui.getFocused(2):
			print('playlist')
			playlist.deselectAll()
			playlist.selectTrack(ModWheel.get_pl_mod_value())

class PitchWheel():
	pitch_value = 0

	def process(event):
		PitchWheel.set_pitch_value(event)

	def set_pitch_value(event):
		PitchWheel.pitch_value = event.data2

	def get_pitch_value():
		return PitchWheel.pitch_value

