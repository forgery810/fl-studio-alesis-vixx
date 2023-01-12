import ui
from utility import Utility
from timing import Timing

class Notes():
	
	root = 0
	upper_limit = -25
	lower_limit = 25
	notes_list = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

	def get_root_note():
		return Notes.root

	def set_root_note(data_two):
		Notes.root = int(Utility.mapvalues(data_two, 0, 11, 0, 127))

	def set_upper_limit(data_two):
		Notes.upper_limit = int(Utility.mapvalues(data_two, -50, 0, 0, 127))

	def set_lower_limit(data_two):
		Notes.lower_limit = int(Utility.mapvalues(data_two, 0, 50, 0, 127))
		
	def get_upper_limit():
		return Notes.upper_limit

	def get_lower_limit():
		return Notes.lower_limit

	def display_limits():
		Timing.begin_message(f"Lower Limit: {Notes.lower_limit} - Upper Limit: {Notes.upper_limit}")

	def root_name(note):
		return Notes.notes_list[note]

class Scales(Notes):

	scale_choice = 0
	major_scales = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26, 28, 29, 31, 33, 35, 36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84, 86, 88, 89, 91, 93, 95, 96, 98, 100, 101, 103, 105, 107, 108, 110, 112, 113, 115, 117, 119, 120, 122, 124, 125, 127, 129, 131, 132, 134, 136, 137, 139, 141, 143, 144]
	natural_scales =[0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26, 27, 29, 31, 32, 34, 36, 38, 39, 41, 43, 44, 46, 48, 50, 51, 53, 55, 56, 58, 60, 62, 63, 65, 67, 68, 70, 72, 74, 75, 77, 79, 80, 82, 84, 86, 87, 89, 91, 92, 94, 96, 98, 99, 101, 103, 104, 106, 108, 110, 111, 113, 115, 116, 118, 120, 122, 123, 125, 127, 128, 130, 132, 134, 135, 137, 139, 140, 142, 144]
	harmonic_scales = [0, 2, 3, 5, 7, 8, 11, 12, 14, 15, 17, 19, 20, 23, 24, 26, 27, 29, 31, 32, 35, 36, 38, 39, 41, 43, 44, 47, 48, 50, 51, 53, 55, 56, 59, 60, 62, 63, 65, 67, 68, 71, 72, 74, 75, 77, 79, 80, 83, 84, 86, 87, 89, 91, 92, 95, 96, 98, 99, 101, 103, 104, 107, 108, 110, 111, 113, 115, 116, 119, 120, 122, 123, 125, 127, 128, 131, 132, 134, 135, 137, 139, 140, 143, 144]
	dorian_scales = [0, 2, 3, 5, 7, 9, 10, 12, 14, 15, 17, 19, 21, 22, 24, 26, 27, 29, 31, 33, 34, 36, 38, 39, 41, 43, 45, 46, 48, 50, 51, 53, 55, 57, 58, 60, 62, 63, 65, 67, 69, 70, 72, 74, 75, 77, 79, 81, 82, 84, 86, 87, 89, 91, 93, 94, 96, 98, 99, 101, 103, 105, 106, 108, 110, 111, 113, 115, 117, 118, 120, 122, 123, 125, 127, 129, 130, 132, 134, 135, 137, 139, 141, 142, 144]
	mixolydian_scales = [0, 2, 4, 5, 7, 9, 10, 12, 14, 16, 17, 19, 21, 22, 24, 26, 28, 29, 31, 33, 34, 36, 38, 40, 41, 43, 45, 46, 48, 50, 52, 53, 55, 57, 58, 60, 62, 64, 65, 67, 69, 70, 72, 74, 76, 77, 79, 81, 82, 84, 86, 88, 89, 91, 93, 94, 96, 98, 100, 101, 103, 105, 106, 108, 110, 112, 113, 115, 117, 118, 120, 122, 124, 125, 127, 129, 130, 132, 134, 136, 137, 139, 141, 142, 144]
	min_pent_scales = [0, 3, 5, 7, 10, 12, 15, 17, 19, 22, 24, 27, 29, 31, 34, 36, 39, 41, 43, 46, 48, 51, 53, 55, 58, 60, 63, 65, 67, 70, 72, 75, 77, 79, 82, 84, 87, 89, 91, 94, 96, 99, 101, 103, 106, 108, 111, 113, 115, 118, 120, 123, 125, 127, 130, 132, 135, 137, 139, 142, 144]
	scales = [major_scales, natural_scales, harmonic_scales, dorian_scales, mixolydian_scales, min_pent_scales]
	scale_names = ["Major", "Natural Minor", "Harmonic Minor", "Dorian", "Mixolydian", "Minor Pentatonic"]

	def set_scale(data_two):
		Scales.scale_choice = int(Utility.mapvalues(data_two, 0, len(Scales.scale_names) - 1, 0, 127))

	def get_scale_choice():
		return Scales.scale_choice

	def scale_message(data_two):
		return ui.setHintMsg(Scales.scale_names[int(mapvalues(self.data_two, 0, len(Scales.scale_names)-1, 0, 127))])

	def scale_name(scale):
		return Scales.scale_names[scale]

	def display_scale():
		return Timing.begin_message(f"Root: {Notes.root_name(Notes.get_root_note())} Scale: {Scales.scale_name(Scales.get_scale_choice())}")