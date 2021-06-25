# fl-studio-alesis-vixx

A MIDI-script for use with the Alesis VI-series(+) keyboards in conjunction with FL Studio

## Installation

- Clone the folder and unzip it to Documents/Image-Line/FL Studio/Settings/Hardware/
- 
- The data.py must be in same folder with the device_alesis... py file. The folder named can be anything. The name in the first line of code of the .py file determines what appears in FL Studio.

- In FL studio under Options/MIDI settings, select the VI61 (or 25/49)(+) under Input. Select "Controller Type" and in the right hand corner you should see the Alesis VIxx option

- Starting with version 0.3 and later VI25 and 49 need two .vi2/.vi4 files to use all of the functionality. The idea is to flip between the two presets to gain access. In step mode the first preset's knobs will affect steps 1-8 and the second preset 9-10. The same with mixer muting, mixer volume, panning and channel volume. 

## Manual

-  soon...


## Notes:

- (+) -> This has only been tested on a VI61 in Windows but the switches should correlate with the other models. Please let me know if you have any issues.

- The .vi6, .vi4 and .vi2 files were created using the Alesis layout editor and are optimized for the script. The 49(.vi4) and 25(.vi2) files are untested but should work. These layouts change the buttons to momentary rather than toggle, lest each has to be pushed twice.






