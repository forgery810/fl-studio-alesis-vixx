

button = {

	"mod_wheel": 1, 			# ok it's not technically a button but it needs to go somewhere 	

    #Transport control switches				
	"record": 114,
	"loop": 115,
	"pattern_down": 116,
	"pattern_up": 117,
	"stop": 118,
	"play": 119,
	

	#First row of switches 
	"undo": 48,							
	"set_metronome": 49,
	"escape": 50,
	"up": 51,
	"browser": 52,
	"rotate_window": 53,				
	"step_editor": 54,
	"blank_three": 55,
	
				
	#Second row of switches 
	"solo": 99,		
	"enter": 65,
	"left": 66,
	"down": 67,
	"right": 68,	
	"blank_four": 69,
	"open_channel_sampler": 70,
	"step_parameter": 71,

	#Third row of switches
	"song_mode_toggle": 80,				
	"overdub": 81,
	"view_playlist": 82,
	"view_piano_roll": 83,
	"view_channel_rack": 84,
	"view_mixer": 85,
	"view_plugin_picker": 86,
	"pad_mode_toggle": 87,
	"pad_one": 60,

}

mode = {
	
	0: "Standard",
	1: "Step Pattern",
	2: "Pad per Channel",

}

parameters = {
	
	0: "Pitch",
	1: "Velocity",
	2: "Release",
	3: "Fine Pitch",
	4: "Panning",
	5: "Mod x",
	6: "Mod y",
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
	"knob_ten":29,
	"knob_eleven":30,
	"knob_twelve":31,
	"knob_thirteen": 32,
	"knob_fourteen": 33,
	"knob_fifteen": 34,
	"knob_sixteen": 35,
}


						##  	Button Layout	 ##


#		  ---		---		---		---		---		---		---		---		---		---		---	
#		   1 		 2 		 3   	 4 		 5 		 6  	 7 		 8 		 9  	 10 	 11 		button number 
#		  ---		---		---		---		---		---		---		---		---		---		---	

#		   48	  	 49 	 50		 51 	 52		 53 	 54 	 55 	 56 	 57 	 58			cc


#		   undo 	metro- 	esc		up 	   rotate   										function
#		   			nome				   window	




#		  ---		---		---		---		---		---		---		---		---		---		---	
#		   17 	 	18 	 	 19 	 20 	 21      22      23      24      25      26      27			button number 
#		  ---		---		---		---		---		---		---		---		---		---		---	

#		   99		 65		 66	  	 67		 68 	 69		 70 	 71 	72 		 73 	 74			cc

#		  solo		enter 	left	down	right			open   rotate								function
#	    											    	chan   mixer/
#																   step
#	   														   	   params




#		  ---		---		---		---		---		---		---		---		---		---		---	
#    	   33        34      35	 	 36 	 37 	 38      39      40      42 	 43  	 44			button number
#		  ---		---		---		---		---		---		---		---		---		---		---	

#    	   80		 81		 82		 83		 84 	 85		 86		 87 	 88 	 89 	 90 		cc

#		  song/     over	play 	piano  channel  mixer 	plugin	 pad								function
#		  pattern	dub		list	 						browser  mode
#		  toggle