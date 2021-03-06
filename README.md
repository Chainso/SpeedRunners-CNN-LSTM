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

The model runs on an April 2016 release of SpeedRunners, when this type of input was supported. Download pyvjoy from https://github.com/tidzo/pyvjoy/. Download and install vJoy and download the feeder SDK from http://vjoystick.sourceforge.net/site/index.php/download-a-install/download. In the feeder SDK folder, go into C# and select your computer architecture. Copy and paste vJoyInterface.dll into your pyvjoy folder, where vjoydevice.py is. Copy that pyvjoy folder to your python/lib/site-packages folder. Download x360ce for 32-bit games from https://www.x360ce.com/. Put x360ce in your SpeedRunners folder where SpeedRunners.exe is. Run vJoyConf.exe which should be in your start menu. If there is only 1 device, click on the 2 tab and click add device. Close vJoyConf and run x360ce. Keep click find settings from internet. Once that is all done, click on game settings and under XInput files, click on all of the 32-bit options. Install all of the other dependencies using pip and you can move on to using the model.

&nbsp;

# Recording Gameplay

Open record_gameplay.py and make sure that the virtual key codes correspond to your gameplay settings. Key codes can be found at https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx. Run record_gameplay.py while you are loaded into the map for SpeedRunners. The best training environment is the practice mode. The window will change to your game when the gameplay starts recording. In order to stop recording, you can close the game or tab out of the game.

&nbsp;

# Training the Model

There is a pre-trained model for nightclub already uploaded, as well as the training data used to train it. The training data used was a very low amount. You can overwrite these or change the model and training data path to create your own. Once you have your training data. Change the batch size to a number that is evenly divisible by the number of pictures in your training data. Change the number of epochs to the number that you want and run train_model.py.

&nbsp;

# Running the model

Once your model is trained, make sure that the model path in play_game.py goes to your trained model. Open the game and load the map you trained on. Run play_game.py, the window will change to your game when the model starts playing.

&nbsp;

# To-Do

Update the input to work with the updated game.
