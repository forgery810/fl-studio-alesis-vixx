# fl-studio-alesis-vixx

A MIDI-script for use with the Alesis VI-series(+) keyboards in conjunction with FL Studio

Youtube Demo: https://www.youtube.com/watch?v=xVxR8Js0qyI

## Installation

- Clone the folder and unzip it to Documents/Image-Line/FL Studio/Settings/Hardware/

- The data.py must be in same folder with the device_AlesisVIxx_1_0_0.py file. The folder named can be anything. The name in the first line of code of the .py file determines what appears in FL Studio.

- In FL studio under Options/MIDI settings, select the VI61 (or 25/49)(+) under Input. Select "Controller Type" and in the right hand corner you should see the Alesis VIxx option. IMPORTANT: MIDIIN2 must be disabled. Only enable VI61 under the Input settings.

- Starting with version 0.3 and later VI25 and 49 need two .vi2/.vi4 files to use all of the functionality. The idea is to flip between the two presets to gain access. In step mode the first preset's knobs will affect steps 1-8 and the second preset 9-16. The same with mixer muting, mixer volume, panning and channel volume. 

- The .vi2/.vi4/.vi6 files labeled for version 0.5 will work with 1.0.

## Manual

-  Note the layout file for button functions. Most of this is self explanatory. A number of the functions are dependent on which window is focused.  

-  Selecting patterns has moved to the transport section and is controlled by the double arrows either direction. The new pattern button has been eliminated.

- The mod wheel figures prominently in this setup. It is used to select channels when channel mode is active and tracks when the mixer is active.
  The directional buttons serve the same purpose but the wheel is much easier to use. 
  
- The enter button is mode dependent. In channel and mixer mode it will toggle the muting of the selected track/channel. In browser mode it will allow the selection and
  assignment of samples and plugins. 
  
- The + knob range button changes the tracks and channels that the knobs can access and the steps the pads can. The button will rotate through ranges 1-16, 17-32, 33-48, and 48-     64. This number of ranges can be reduced will some simple code changes if desired for simplicity.

- The mouse should be moved to a neutral section of the FL layout. If it is over a knob or step, for example, the text on the top left will not display info necessary to know       which mode you are in.


##       Mixer Mode
 
-  When the mixer is focused again the mod wheel will scroll through the tracks. Enter toggles mute for the selected channel and solo works as expected. The knobs will control the track level for corresponding track.
   If the master track is highlighted any knob will control the master volume but will revert back to the standard setup once another track is selected. The knob must first equal the tracks current position before it engages to prevent jumping of values. Pressing the step/mixer options button will change the mode. Panning mode will change the knob control to panning with the same behaviour as the level control. Knob/Range can increase the track number the knobs control. 

##      Channel Mode

- When the channel window is focused, the mod wheel controls channel selection. As with the mixer, mute and solo work as well as the knob control over channel volume. 

- Pressing the pad mode button will rotate through the pad options. Standard plays the selected channels notes as expected. Step mode controls the selected channel as a 
  16 step sequencer. In pad per channel mode each pad individually controls up to the first 16 channels.
  
  ##       - Step Sequencer Mode
  
  - In step sequencer mode the channels can be selected and the pads will add or remove steps accordingly. The step mode options button above the pad option button now rotates 
    through the various step parameters - pitch, velocity, release, fine pitch, panning, x value, and y value. The knobs will control the parmater value for each step of the         current track. Release seems to have no effect. Shift does not function well currently so it is not included. 
    
  - The knob/range button will increase the steps the pads and knobs control by 16 with each push. Up to 64 steps can be contorlled this way.
    
## Broswer Mode

-  Selecting the browser button will allow the directional keys to control the selection of samples. Right opens folders and left closes them. Enter will bring up the menu for what to do with the selection. Unfortunatley, when selecting open in new channel the browser loses focus because the channel window open so the browser button must be pushed again. Selecting the browser button again will close the browser window but it cannot be opened again, unfortunately, without using the mouse. This functionality is a little cumbersome unfortunately, but can still be useful.
  
## Plugins

- When a plugin is in focus, the knobs will control some of its functionality. The knob range can be increased to access more parameters. Unfortunately, the default order is set by FL or the plugin maker, so for plugins with a high number of parameters, it is not realistic to use. For lower parameter plugins (Fruity Granulizer and Tranistor Bass e.g.) it is very functional, though. 

- The double arrow buttons that usually control the pattern number will rotate through plugin presets when a plugin is focused. This will not work with "internal" presets, as found in older FL Studio plugins. It will work with presets saved under the plugin option arrow in the window. For example, Flex and Ogun work outright but in Poizone the presets within the plugin itself will not rotate so you will have to save the ones you want using the window option.  

 ## VI25 and VI49 Users
 
 - Extra layouts are included for these two formats. The second layout will allow control over the steps, channels and tracks 9-16. These two presets should be uploaded in slots
   right next to each other so they can be quickly rotated between. In the case of the VI25, the first layout will control steps/tracks 1-8 and the second will control 9-16. If the range is increased, then the first layout will control 17-22 and the second 28-32, etc.
  

## Notes:

- (+) -> This has only been tested on a VI61 in Windows but the switches should correlate with the other models. Please let me know if you have any issues.

- The .vi6, .vi4 and .vi2 files were created using the Alesis layout editor and are optimized for the script. The 49(.vi4) and 25(.vi2) files are untested but should work. These layouts change the buttons to momentary rather than toggle, lest each has to be pushed twice.






