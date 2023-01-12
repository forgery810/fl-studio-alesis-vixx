import ui
from config import Config

class Timing():

	count = 0
	msg_start = 0
	post_msg = False
	message = ''

	def update_counter():
		Timing.count += 1
		Timing.check_msgs()	

	def check_msgs():
		if Timing.get_count() >= Config.MSG_LENGTH  + Timing.msg_start:
			Timing.post_msg = False
		else:
			Timing.send_msg(Timing.message)

	def get_count():
		return Timing.count

	def begin_message(m):
		Timing.message = m
		Timing.post_msg = True
		Timing.msg_start = Timing.get_count()

	def send_msg(m):
		ui.setHintMsg(m)
