import numpy as np
import pywintypes
import os

from cnn_lstm import CNNLSTM
from info_grabber import InfoGrabber
from actor import Actor


#-----Constants-----#
# The width of the image
IMAGE_WIDTH = 128

# The height of the image
IMAGE_HEIGHT = 128

# The depth of the iamge
IMAGE_DEPTH = 1

# The name of the process
PROCESS_NAME = "SpeedRunners.exe"

# Current Directory
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

# The path to save the model
MODEL_PATH = CURRENT_DIR + "/SpeedRunners Models/nightclub_model.ckpt"


#-----Get the classes-----#

# Create the CNN-LSTM
model = CNNLSTM(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_DEPTH)

# Load trained model
model.load(MODEL_PATH)

# The info grabber
info = InfoGrabber(PROCESS_NAME)

# The actor
actor = Actor()

# All the possible actions
ACTIONS = {0 : actor.left,
           1 : actor.left_boost,
           2 : actor.right,
           3 : actor.right_boost,
           4 : actor.jump,
           5 : actor.jump_boost,
           6 : actor.jump_left,
           7 : actor.jump_left_boost,
           8 : actor.jump_right,
           9 : actor.jump_right_boost,
           10 : actor.grapple,
           11 : actor.grapple_left,
           12 : actor.grapple_right,
           13 : actor.item,
           14 : actor.item_boost,
           15 : actor.item_left,
           16 : actor.item_left_boost,
           17 : actor.item_right,
           18 : actor.item_right_boost,
           19 : actor.slide}


print("Now playing\n")

while(True):
    try:
        # Get the screenshot from the game
        screenshot = np.array([info.np_screenshot(IMAGE_WIDTH, IMAGE_HEIGHT)])

        # Get the output from the model
        out = model.get_out(screenshot)

        # Get the best action
        action = np.argmax(out)

        # Perform the action
        ACTIONS[action]()

    # Will keep playing until the player closes the game or changes tab
    except pywintypes.error:
        break

print("Done Playing")

# Reset all buttons
actor.reset_vjoy()
actor.reset()
actor.reset_buts()
actor.reset_boost()
