import os
import numpy as np
from cnn_lstm import CNNLSTM

#-----Classes and Constants-----#

# The learning rate
LR = 0.00005

# The width of the image
IMAGE_WIDTH = 128

# The height of the image
IMAGE_HEIGHT = 128

# The number of epochs
EPOCHS = 7

# The batch size (make sure that the length of the training data is evenly
# divisible by this number)
BATCH_SIZE = 184

# The number of memory frames (make sure that 20 is evenly divisIble by this
# number)
MEMORY_FRAMES = 10

# The name of the process
PROCESS_NAME = "SpeedRunners.exe"

# Current Directory
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

# The path for the data
DATA_PATH = CURRENT_DIR + "/SpeedRunners Training Data/training_data.npy"

# The path to save the model
MODEL_PATH = CURRENT_DIR + "/SpeedRunners Models/model.ckpt"


#-----Train Model-----#

# CNN-LSTM Model
model = CNNLSTM(IMAGE_WIDTH, IMAGE_HEIGHT, 1, BATCH_SIZE, MEMORY_FRAMES, LR)

# Get the data
data = np.load(DATA_PATH)

# Load the model if it exists
model.load(MODEL_PATH)

# Train the model
model.train(data, EPOCHS)

# Save the model
model.save(MODEL_PATH)

# Test the model
model.test(data)