# SpeedRunners-CNN-LSTM

CNN-LSTM Network that learns to play SpeedRunners.

&nbsp;

# Dependencies

vJoy

pyvjoy

x360ce

tensorflow

numpy

cv2

pathlib

win32gui

win32ui

win32con

win32api

win32process

ctypes

pywintypes

psutil

&nbsp;

# Setup

The model runs on an April 2016 release of SpeedRunners, when this type of input was supported. Download pyvjoy from https://github.com/tidzo/pyvjoy/. Download and install vJoy and download the feeder SDK from http://vjoystick.sourceforge.net/site/index.php/download-a-install/download. In the feeder SDK folder, go into C# and select your computer architecture. Copy and paste vJoyInterface.dll into your pyvjoy folder, where vjoydevice.py is. Copy that pyvjoy folder to your python/lib/site-packages folder. Download x360ce for 32-bit games from https://www.x360ce.com/. Put x360ce in your SpeedRunners folder where SpeedRunners.exe is. Run vJoyConf.exe which should be in your start menu. If there is only 1 device, click on the 2 tab and click add device. Close vJoyConf and run x360ce. Keep click find settings from 

&nbsp;

# Recording Gameplay

To record your own gameplay, run record_gameplay.py while you are loaded into the map for SpeedRunners. The best training environment is the practice mode. The window will change to your game when the gameplay starts recording. In order to stop recording, you can close the game or tab out of the game.

&nbsp;

# Training the Model

There is a pre-trained model for nightclub already uploaded, as well as the training data used to train it. The training data used was a very low amount. You can overwrite these or change the model and training data path to create your own. Once you have your training data

&nbsp;

# To-Do

Update the input to work with the updated game.
