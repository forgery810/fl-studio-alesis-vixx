# fl-studio-alesis-vixx

A MIDI-script for use with the Alesis VI-series(*) keyboards in conjunction with FL Studio

## Installation

- Place the .py file into a new folder (the name of which is your choice) into the following directory Documents/Image-Line/FL Studio/Settings/Hardware/

- In FL studio under Options/MIDI settings, select the VI61 (or 25/49) under Input. Select "Controller Type" and in the right hand corner you should see the Alesis VIxx option

## Notes:

- (*) This has only been tested on a VI61 in Windows but the switches should correlate with the other models. Please let me know if you have any issues.

- See the .jpg file for the layout of buttons. This was created with the standard VI MIDI layout installed. The CC numbers should correlate. I would recommend changing all switches to momentary rather than the default toggle. If left in the toggle state, you will have to push switches twice.

- Currently Knob 1 is hardcoded to control the selected channel volume in the channel settings and not in the mixer. The should be fixed in a later version. If you prefer this to not be the case then you can see the notes in the .py file where you can edit this functionality out.

- This is a very early version aimed at getting the basics working on this keyboard. Given the number of buttons to work with, a lot of functionality can be added. I hope to update again soon. Please let me know if you have any feedback.




