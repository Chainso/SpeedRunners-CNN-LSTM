import numpy as np
import win32api as wapi
import pywintypes
import os
from info_grabber import InfoGrabber

# Going to sort keys by priority (grapple -> jump -> item -> slide -> left -> right)
vk_to_key = {0x53 : "grapple",
             0x41 : "jump",
             0x44 : "item",
             0x28 : "slide",
             0x20 : "boost",
             0x25 : "left",
             0x27 : "right"}

# All the possible actions and their corresponding one hot vector
action_to_one_hot = {"left" : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "left_boost" : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "right" : [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "right_boost" : [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "jump" : [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "jump_boost" : [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "jump_left" : [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "jump_left_boost" : [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "jump_right" : [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "jump_right_boost" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "grapple" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "grapple_left" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                     "grapple_right" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                     "item" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                     "item_boost" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                     "item_left" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                     "item_left_boost" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                     "item_right" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                     "item_right_boost" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                     "slide" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}


def key_check():
    keys = []
    for key in vk_to_key:
        if(wapi.GetAsyncKeyState(key) and key in vk_to_key):
            keys.append(vk_to_key[key])

    # Convert to proper movements
    end = ""

    if("boost" in keys):
        end = "_boost"
        keys.pop(keys.index("boost"))

    # No action should be the same as sliding
    if(len(keys) == 0 or keys[0] == "slide"):
        keys = ["slide"]
    elif(len(keys) == 1 or keys[0] == "left" or keys[0] == "right"):
        keys = [keys[0]]
    else:
        # Direction is always the last two keys
        direction = find_direction(keys[-2:])

        keys = [keys[0] + "_" + direction] if direction != "" else [keys[0]]

    keys[0] = keys[0] + end

    if(("slide" in keys[0] or "grapple" in keys[0]) and "_boost" in keys[0]):
        keys[0] = keys[0].replace("_boost", "")


    keys[0] = action_to_one_hot[keys[0]]


    return np.array(keys)

def find_direction(keys):
    direction_found = False
    direction = ""

    i = 0

    while(not direction_found and i < len(keys)):
        if(keys[i] == "left" or keys[i] == "right"):
            direction_found = True
            direction = keys[i]

        i += 1

    return direction

# The name of the process
PROCESS_NAME =  "SpeedRunners.exe"

# The width of the image
IMAGE_WIDTH = 128

# The width of the height
IMAGE_HEIGHT = 128

# Current Directory
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

# The path for the data
DATA_PATH = CURRENT_DIR + "/SpeedRunners Training Data/nightclub_data.npy"

# Module to get the screenshots
info = InfoGrabber(PROCESS_NAME)

# Use this if you are appending to old data
#data = np.load(DATA_PATH)

# The total data
data = []

# The data from this session of recording
new_data = []

while(True):
    try:
        screenshot = info.np_screenshot(IMAGE_WIDTH, IMAGE_HEIGHT)
        action = key_check()

        new_data.append([screenshot, action])
        
    # Keep running until game is closed or window is changed
    except pywintypes.error:
        break

new_data = np.array(new_data)

if(len(data) == 0):
    data = new_data
else:
    # Append the data together if there was old data
    data = np.append(data, new_data, 0)

# Printing the data shape so you know what to set the batch size to for
# training
print(data.shape, "\n")

print("Saving data to", DATA_PATH)

# Save the data
np.save(DATA_PATH, data)
