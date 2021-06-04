# fl-studio-alesis-vixx

A MIDI-script for use with the Alesis VI-series(*) keyboards in conjunction with FL Studio

## Installation

- Clone the folder and unzip it to Documents/Image-Line/FL Studio/Settings/Hardware/

- The .py file is the only file that needs to be there but FL should ignore the other files without issue. The folder name can be anything. The name in the first line of code of the .py file determines what appears in FL Studio.

- In FL studio under Options/MIDI settings, select the VI61 (or 25/49)(+) under Input. Select "Controller Type" and in the right hand corner you should see the Alesis VIxx option

## Notes:

- (+) -> This has only been tested on a VI61 in Windows but the switches should correlate with the other models. Please let me know if you have any issues.

- The .vi6 file is the recommended configuration for the 61 key version of the keyboard. I suspect it will not work with the vi25 or vi49. This will turn the switches to momentary and resolve a conflict between the sustain and button 17 which will both open a new pattern in the default config. If you do not use a sustain pedal this will not be an issue. If you need to change it manually, use the Alesis program to change the sustain CC to 96, in addition to the button type to momentary for each.

- See the .jpg file for the layout of buttons. Again, I would recommend changing all switches to momentary rather than the default toggle. If left in the toggle state, you will have to push switches twice.

- Currently Knob 1 is hardcoded to control the selected channel volume in the channel settings and not in the mixer. The should be fixed in a later version. If you prefer this to not be the case then you can see the notes in the .py file where you can edit this functionality out.

- This is a very early version aimed at getting the basics working on this keyboard. Given the number of buttons to work with, a lot of functionality can be added. I hope to update again soon. Please let me know if you have any feedback.




