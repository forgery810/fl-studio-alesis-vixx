# fl-studio-alesis-vixx

A MIDI-script for use with the Alesis VI-series(*) keyboards in conjunction with FL Studio

## Installation

- Clone the folder and unzip it to Documents/Image-Line/FL Studio/Settings/Hardware/

- The .py file is the only file that needs to be there but FL should ignore the other files without issue. The folder name can be anything. The name in the first line of code of the .py file determines what appears in FL Studio.

- In FL studio under Options/MIDI settings, select the VI61 (or 25/49)(+) under Input. Select "Controller Type" and in the right hand corner you should see the Alesis VIxx option

## Notes:

- (+) -> This has only been tested on a VI61 in Windows but the switches should correlate with the other models. Please let me know if you have any issues.

- The .vi6, .vi4 and .vi2 files were created using the Alesis layout editor and are optimized for the script. The 49(.vi4) and 25(.vi2) files are untested but should work. These layouts change the buttons to momentary rather than toggle, lest each has to be pushed twice. Additionally, the default Alesis layout has a conflict between the sustain CC and button 17 CC, both of which are set to 64 and would open a new pattern when the scrpit is used. This addresses that by changing the CC of the sustain to 96.

- See the .jpg file for the layout of buttons. If one wished to change the layout, use the Alesis editor and change the button CC to the one of the function you would like it to in the .py file.

- Currently Knob 1 is hardcoded to control the selected channel volume in the channel settings and not in the mixer. The should be fixed in a later version. If you prefer this to not be the case then you can see the notes in the .py file where you can edit this functionality out.

- This is a very early version aimed at getting the basics working on this keyboard. Given the number of buttons to work with, a lot of functionality can be added. I hope to update again soon. Please let me know if you have any feedback.




