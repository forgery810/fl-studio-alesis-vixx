import _random
import ui 
from timing import Timing

class Utility():

	def num_gen():
		"""returns random interger based on 16 bit seed"""

		rand_obj = _random.Random()
		rand_obj.seed()
		rand_int = rand_obj.getrandbits(16) 
		return rand_int 

	def mapvalues(value, tomin, tomax, frommin, frommax):
		input_value = value
		solution = tomin + (tomax-(tomin))*((input_value - frommin) / (frommax - (frommin)))
		if  -0.01 < solution < 0.01:
			solution = 0
		return solution



	



