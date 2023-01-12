
class Config():

	# If True, Knobs will only control selected channel/track. 1 - Level. 2 - Panning. 3 - Channel To Track Routing (Channels only) 
	ALT_ALWAYS = False

	# If True, Pitch Wheel will always alter pitch of selected channel unless Shift button is set.
	PITCH_BEND_ON = True

	# This controls how long messages persist in the hint panel
	MSG_LENGTH = 75				

	# You can have as many or as few colors as you like in this list. 
	# Use a color picker, convert the hex value to decimal, and add it to the list with a - in front.	
	COLORS = [-10721942, -5808209, -10849336, -13462158, -13030268, -13462136, -10900811, -7293607, -4879527, -5545351, -12619400]

	# This number sets the max track the mod wheel can reach in the Playlist. A lower number allows less access but easier precision.
	PLAYLIST_REACH = 40