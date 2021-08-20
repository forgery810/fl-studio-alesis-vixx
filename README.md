# fl-studio-alesis-vixx

A MIDI-script for use with the Alesis VI-series(+) keyboards in conjunction with FL Studio

## Installation

- Clone the folder and unzip it to Documents/Image-Line/FL Studio/Settings/Hardware/

- The data.py must be in same folder with the device_alesis... py file. The folder named can be anything. The name in the first line of code of the .py file determines what appears in FL Studio.

- In FL studio under Options/MIDI settings, select the VI61 (or 25/49)(+) under Input. Select "Controller Type" and in the right hand corner you should see the Alesis VIxx option

- Starting with version 0.3 and later VI25 and 49 need two .vi2/.vi4 files to use all of the functionality. The idea is to flip between the two presets to gain access. In step mode the first preset's knobs will affect steps 1-8 and the second preset 9-10. The same with mixer muting, mixer volume, panning and channel volume. 

- The .vi2/.vi4/.vi6 files labeled for version 0.5 will work with 1.0.

## Manual

-  Note the data.py file for button functions. Most of this is self explanatory. A number of the functions are dependent on which window is focused. 

-  Selecting patterns has moved to the transport section and is controlled by the double arrows either direction. The new pattern button has been eliminated.

- The mod wheel figures prominently in this setup. It is used to select channels when channel mode is active and tracks when the mixer is active.
  The directional buttons serve the same purpose but the wheel is much easier to use. 
  
- The enter button is mode dependent. In channel and mixer mode it will toggle the muting of the selected track/channel. In browser mode it will allow the selection and
  assignment of samples and plugins. 


##       Mixer Mode
 
-  When the mixer is focused again the mod wheel will scroll through the tracks. Mute and solo will work accordingly. The knobs will control the track level for each initially.
   If the master track is highligthed the first knob will control master and the second knob will control the first track etc but will revert back to the standard setup once        another track is selected. The knob must first equal the tracks current position before it engages to prevent jumping of values. Pressing the step/mixer options button will      change the mode. Panning mode will change the knob control to panning with the same behaviour as the level control. Mute mode makes the buttons of the first row mute their      respsective track. (This mode will likely be removed in a later version or replaced with control over record arming.)

##      Channel Mode

- When the channel window is focused, the mod wheel controls channel selection. As with the mixer, mute and solo work as well as the knob control over channel volume. 

- Pressing the pad mode button will rotate through the pad options. Standard plays the selected channels notes as expected. Step mode controls the selected channel as a 
  16 step sequencer. In channel mode each pad individually controls up to the first 16 channels.
  
  ##       - Step Sequencer Mode
  
  - In step sequencer mode the channels can be selected and the pads will add or remove steps accordingly. The step mode options button above the pad option button now rotates 
    through the various step parameters - pitch, velocity, release, fine pitch, panning, x value, and y value. The knobs will control the parmater value for each step of the         current track. Release seems to have no effect. Shift does not function well currently so it is not included.
    
## Broswer Mode

- The browser must be detached (for an unknown reason) for this mode to work. Selecting the browser button allow the directional keys to control the selection of samples.       Right opens folders and left closes them. Enter will bring up the menu for what to do with the selection. Unfortunatley, when selecting open in new channel the browser loses     focus because the channel window open so the browser button must be pushed again. It is a little more cumbersome than preferred but it is functional.
  

 ## vi25 and vi49 Users
 
 - Extra layouts are included for these two formats. The second layout will allow control over the steps, channels and tracks 9-16. These two presets should be uploaded in slots
   right next to each other so they can be quickly rotated between.
  

## Notes:

- (+) -> This has only been tested on a VI61 in Windows but the switches should correlate with the other models. Please let me know if you have any issues.

- The .vi6, .vi4 and .vi2 files were created using the Alesis layout editor and are optimized for the script. The 49(.vi4) and 25(.vi2) files are untested but should work. These layouts change the buttons to momentary rather than toggle, lest each has to be pushed twice.






