import arrangement
import transport
import midi
import ui
import channels
import plugins
import device
import patterns
from data import mode
from switch import Switch
from config import *
from plugindata import *

offset = [0, 16, 32, 48]
temp_step = [0]

class Pads(Switch):

	def pad_hit(event):

		if event.midiId == 144:
			temp_step.clear()
			temp_step.append(event.data1 + offset[Switch.offset_iter])
		# print(f'temp step: {temp_step}')

		if ui.getFocused(5) and plugins.isValid(channels.selectedChannel()):
			if event.midiId == 128 and event.data2 != 0:
				print('skip')
			elif plugins.getPluginName(channels.selectedChannel()) == 'FPC' and event.data1 in alesis_pads:
				print('FPC')
				channels.midiNoteOn(channels.selectedChannel(), FPC_pads[alesis_pads.index(event.data1 + offset[Switch.offset_iter])], event.data2)
				event.handled = True


		elif Switch.mode_toggle == 1 and event.midiId == 144:						
			if channels.getGridBit(channels.selectedChannel(), event.data1 - 60 + offset[Switch.offset_iter]) == 0:						
				channels.setGridBit(channels.selectedChannel(), event.data1 - 60 + offset[Switch.offset_iter], 1)	
				event.handled = True
																						
			else:															
				channels.setGridBit(channels.selectedChannel(), event.data1 - 60 + offset[Switch.offset_iter], 0)    
				event.handled = True	

		elif Switch.mode_toggle == 2  and 60 <= event.data1 < (channels.channelCount() + 60):
			# print(Switch.get_pad_mode)
			# print(Switch.pitch_num)
			channels.setChannelPitch(event.data1-60,  mapvalues(Switch.pitch_num, -1, 1, 0, 127))
			channels.selectOneChannel(event.data1-60)  
			channels.midiNoteOn(event.data1-60, 60, event.data2, Switch.pitch_num)
			print('a pad has been hit')
			event.handled = True

		# else:
		# 	if PITCH_WHEEL == True:
		# 		channels.setChannelPitch(channels.selectedChannel(),  mapvalues(Switch.pitch_num, -1, 1, 0, 127))
				
		# 	# print(device.getLinkedValue(event.data1))
		# 	channels.midiNoteOn(channels.selectedChannel(), event.data1, event.data2)

		
def mapvalues(value, tomin, tomax, frommin, frommax):
	input_value = value
	solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
	if  -0.01 < solution < 0.01:
		solution = 0
#	print(f"Solution: {solution}")
	return solution





# this code was used to acquire plugin parameter names/numbers and store them in a dictionary
		# plug_param_gen(plugins.getParamCount(channels.selectedChannel()), )
		# plug_dict = {}
		# count = plugins.getParamCount(channels.selectedChannel())
		# store = []

		# for i in range(count):
		# 	name = plugins.getParamName(i, channels.selectedChannel())
		# 	store.append(name)
		# # print(store)
		# plug_dict = dict(list(enumerate(store)))
		# print(plug_dict)

		# param_names = [i for i in plugins.getParamName(channels.selectedChannel)]
