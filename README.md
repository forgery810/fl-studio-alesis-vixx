# fl-studio-alesis-vixx

A MIDI-script for use with the Alesis VI-series(+) keyboards in conjunction with FL Studio

Youtube Demo: https://www.youtube.com/watch?v=xVxR8Js0qyI

Image Line forum entry for this script: https://forum.image-line.com/viewtopic.php?f=1994&t=247069

                   
Update to 1.5   -> - generator now uses pitch wheel to determine likelihood of trigs being generated. Moving the pitch up lowers the number while down fills every step.
                   - Random note generator with scales and range control has been added.
                   - There is a new step parameter edit mode that allows VI49 and 25 users to edit steps without having to use a second Alesis layout
                   - Pads now mapped to FPC when loaded
                   - Channels can now be linked to mixer track
                   - The color of tracks and channels can now be changed
                   - On VI61, buttons 12-16 jump to patterns 1-5 and buttons go to 6-10 respectively
                   - A number of plugins have knobs auto-mapped
                   - Script has been re-organized 
                   - See version document for more info

                             
Update to 1.52 -> - Fixed some bugs and expanded FPC pad access

Update to 1.54 -> - Fixed issue where solo button was not functions correctly in mixer mode
                  - Cleaned up code

## Installation

- Update to the latest version of FL Studio before installing. Some conflicts may occur in 20.7.x versions in particular. See troubleshooting below if you have issues. 

- Clone the folder and unzip it to Documents/Image-Line/FL Studio/Settings/Hardware/  (put the folder here, not just the files)

- All .py must be in same folder with the device_AlesisVIxx_1_0_2.py file. The folder named can be anything. The name in the first line of code of the .py file determines what appears in FL Studio.

- In FL studio under Options/MIDI settings, with the keyboard connected, select the VI61 (or 25/49)(+) under Input. Select "Controller Type" and in the right hand corner you should see the Alesis VIxx option. IMPORTANT: MIDIIN2 must be disabled. Only enable VI61 under the Input settings.

- Starting with version 0.3 and later VI25 and 49 need two .vi2/.vi4 files to use all of the functionality. The idea is to flip between the two presets to gain access to everything the VI61 has. In step mode the first preset's knobs will affect steps 1-8 and the second preset 9-16. The same with mixer muting, mixer volume, panning and channel volume. 

  With version 1.5 and the new parameter edit mode, step editing no longer needs two layouts to access all steps. Some of the news functions, including random, will need an edit of the layout or a second one to be able to accessed. 
 
 - 1.5 comes with a new layout that needs to be used with the VI61 and 49 for the Shift button to function correctly. Upload it or use the Alesis program to change the Shift     
   button to a toggle rather than momentary.
 


## Manual

-  Note the layout file for button functions. Most of this is self explanatory. A number of the functions are dependent on which window is focused.  

-  Selecting patterns has moved to the transport section and is controlled by the double arrows either direction. The new pattern button has been eliminated from previous          versions.

- The mod wheel figures prominently in this setup. It is used to select channels when channel mode is active and tracks when the mixer is active. The directional buttons serve     the same purpose but the wheel is much easier to use. 
  
- The enter button is mode dependent. In channel and mixer mode it will toggle the muting of the selected track/channel. In browser mode it will allow the selection and
  assignment of samples and plugins. 
  
- The + knob range button changes the tracks and channels that the knobs can access and the steps the pads can. The button will rotate through ranges 1-16 and 17-32. The range  
  options have been reduced to make the script easier to use. This can be altered in the code.

- The mouse should be moved to a neutral section of the FL layout. If it is over a knob or step, for example, the text on the top left will not display info necessary to know     which mode you are in. 


##       Mixer Mode
 
- When the mixer is focused again the mod wheel will scroll through the tracks. Enter toggles mute for the selected channel and solo works as expected. The knobs will control     the track level for corresponding track.

  If the master track is highlighted the first knob will control the master volume but will revert back to the standard setup once another track is selected. The knob must         first equal the tracks current position before it engages to prevent jumping of values. Pressing the step/mixer options button will change the mode. Panning mode will change     the knob control to panning with the same behaviour as the level control. Knob/Range can increase the track number the knobs control. 
 
- To link channel to a mixer track, highlight the channel you want to link, then push the mixer button and highlight the mixer channel you wish to link it to. Then push the       link button.
 
- Color button can be selected to rotate through a set sequence of colors.

##      Channel Mode

-  When the channel window is focused, the mod wheel controls channel selection. As with the mixer, mute and solo work as well as the knob control over channel volume. 

-  Pressing the pad mode button will rotate through the pad options. Standard plays the selected channels notes as expected. Step mode controls the selected channel as a 
   16 step sequencer. In pad per channel mode each pad individually controls up to the first 16 channels.
   
 - The color button functions the same here as in mixer mode.
  
  ##       - Step Sequencer Mode
  
  - In step sequencer mode the channels can be selected and the pads will add or remove steps accordingly. The step mode options button above the pad option button now rotates 
    through the various step parameters - pitch, velocity, release, fine pitch, panning, x value, and y value. The knobs will control the parmater value for each step of the         current track. Release seems to have no effect. Shift does not function well currently so it is not included. 
    
  - The knob/range button will increase the steps the pads and knobs control by 16 with each push. Up to 64 steps can be contorlled this way.

  - Currently, this only functions when all channels are shown. If some are hidden in groups, it will not work.
  
  ##       - Parameter Edit Mode
  
  - The fourth option under pad mode allows editing of steps, one at a time. When in the mode, press the pad of the step you want to edit. Now the first 7 knobs control the 
    parameters for that step (pitch, velocity, release, etc). This eliminates the need for a second Alesis layout to access all steps for VI49 and 25 users.
    
  ##      - Random
  
  - The random pattern button on VI49 and VI61 will generate a random step sequence. Use the pitch wheel to determine the likelihood of each step being triggered. Down increases     the number of steps set. Pushing the wheel all the way up is a way to clear the pattern.

  - The random note generator will change the pitch of every step a random note in the selected key. With shift mode set, the first four knobs can be used to edit the scale.         The first knob controls the note and the second control decides the scale. The third and fourth knob control the low and high end of the note range. 
    
## Broswer Mode

-  Selecting the browser button will allow the directional keys to control the selection of samples. Right opens folders and left closes them. Enter will bring up the menu for what to do with the selection. Unfortunatley, when selecting open in new channel the browser loses focus because the channel window open so the browser button must be pushed again. Selecting the browser button again will close the browser window but it cannot be opened again, unfortunately, without using the mouse. This functionality is a little cumbersome unfortunately, but can still be useful.
  
## Plugins

- When a plugin is in focus, the knobs will control some of its functionality. The knob range can be increased to access more parameters. Some of the plugins have layouts preset   in the script for better functionality. 

- The double arrow buttons that usually control the pattern number will rotate through plugin presets when a plugin is focused. This will not work with "internal" presets, as     found in older FL Studio plugins. It will work with presets saved under the plugin option arrow in the window. For example, Flex and Ogun work outright but in Poizone the       presets within the plugin itself will not rotate so you will have to save the ones you want using the window option.  

 ## VI25 and VI49 Users
 
 - Extra layouts are included for these two formats. The second layout will allow control over the steps, channels and tracks 9-16. These two presets should be uploaded in slots
   right next to each other so they can be quickly rotated between. In the case of the VI25, the first layout will control steps/tracks 1-8 and the second will control 9-16. If    the range is increased, then the first layout will control 17-22 and the second 28-32, etc.
  
## Troubleshooting

- Update FL Studio before you do anything else. If you are on a cracked/illegal copy of FL Studio, please do not ask for help with any problems and go buy FL Studio.

- Most problems have arisen from the folder not being in the right location and the data.py not being present.

- Make sure user data folder is set to the default location \Documents\Image Line. If you have it set elsewhere and want to keep it that way, clone the folder to the             
  corresponding place ...\Settings\Hardware

- If you are still having an issue, on FL Studio go to View - Script Output, hit a few buttons on the Alesis and copy what is there. Then create an issue on github or respond on 
  the Image Line forum entry (link above) for this controller. Describe the issue and paste the results from the Script Output.

## Notes:

- (+) -> This has only been tested on a VI61 in Windows but the switches should correlate with the other models. Please let me know if you have any issues.

- The .vi6, .vi4 and .vi2 files were created using the Alesis layout editor and are optimized for the script. The 49(.vi4) and 25(.vi2) files are untested but should work.

## Bugs

- When the master track is selected in Mixer, other tracks do not respond appropriately to knob turns

