import tensorflow as tf
import numpy as np
import os
from tensorflow.contrib import rnn

class CNNLSTM():
    def __init__(self, width, height, input_channels, batch_size=1,
                 memory_frames=10, learning_rate=0.0001):

        # Stop the tensorflow debugging
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

        # The batch size
        self.batch_size = batch_size

        # The number of memory frames
        self.memory_frames = memory_frames

        # The width
        self.width = width

        # The height
        self.height = height

        # The number of input channels
        self.input_channels = input_channels

        # The input image from Speedrunners
        self.inp = tf.placeholder(tf.float32,
                                  (None, width, height, input_channels),
                                  name = "input")
        # The output labels
        self.labels = tf.placeholder(tf.float32, (None, 1, 20),
                                     name = "labels")

        # The first convolutional layer (inp -> conv1)
        self.conv1 = tf.layers.conv2d(inputs = self.inp,
                                 filters = 24,
                                 kernel_size = 7,
                                 strides = 3,
                                 padding = "VALID",
                                 activation = tf.nn.relu,
                                 name = "conv1")
        
        # The second convolutional layer (conv1 -> conv2)
        self.conv2 = tf.layers.conv2d(inputs = self.conv1,
                                 filters = 32,
                                 kernel_size = 5,
                                 strides = 2,
                                 padding = "VALID",
                                 activation = tf.nn.relu,
                                 name = "conv2")
        
        # The third convolutional layer (conv2 -> conv3)
        self.conv3 = tf.layers.conv2d(inputs = self.conv2,
                                 filters = 64,
                                 kernel_size = 3,
                                 strides = 2,
                                 padding = "VALID",
                                 activation = tf.nn.relu,
                                 name = "conv3")
        
        # The fourth convolutional layer (conv3 -> conv4)
        self.conv4 = tf.layers.conv2d(inputs = self.conv3,
                                 filters = 128,
                                 kernel_size = 3,
                                 strides = 1,
                                 padding = "VALID",
                                 activation = tf.nn.relu,
                                 name = "conv4")

        # The fifth convolutional layer (conv4 -> conv5)
        self.conv5 = tf.layers.conv2d(inputs = self.conv4,
                                 filters = 256,
                                 kernel_size = 2,
                                 strides = 1,
                                 padding = "VALID",
                                 activation = tf.nn.relu,
                                 name = "conv5")

        # The sixth convolutional layer (conv5 -> conv6)
        self.conv6 = tf.layers.conv2d(inputs = self.conv5,
                                 filters = 256,
                                 kernel_size = 2,
                                 strides = 1,
                                 padding = "VALID",
                                 activation = tf.nn.relu,
                                 name = "conv6")


        # The reshaped output from the convolution (conv6 -> flattened_conv)
        self.reshaped_conv = tf.reshape(self.conv6,
                                        (self.batch_size, self.memory_frames,
                                         (5 * 5 * 256) // self.memory_frames),
                                        name = "flattened_conv")

        # 3 LSTM cells (flattened_conv -> LSTM)
        self.lstm = [rnn.BasicLSTMCell(n) for n in [256, 128, 64]]

        # Convert the 3 cells to a MultiCell
        self.lstm = rnn.MultiRNNCell(self.lstm)

        # The cells' initial state
        self.cell_init_state = self.lstm.zero_state(self.batch_size,
                                                    dtype = tf.float32)

        # The output of the LSTM
        self.lstm_out = tf.nn.dynamic_rnn(cell=self.lstm,
                                          inputs=self.reshaped_conv,
                                          initial_state=self.cell_init_state)[0]

        # First dense layer (LSTM -> dense1)
        self.dense1 = tf.layers.dense(inputs = self.lstm_out,
                                      units = 20 // self.memory_frames,
                                      activation = None,
                                      name = "dense1")

        # Flattened dense output (dense1 -> flattened_dense) (20 actions)
        self.flattened_dense = tf.reshape(self.dense1, (-1, 1, 20),
                                          name = "flattened_dense")

        # The output of the network
        self.prediction = tf.nn.softmax(self.flattened_dense,
                                        name = "prediction")

        # Using softmax cross entropy loss
        self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.flattened_dense, labels=self.labels))

        # Adam optimizer to minimize the loss
        self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.loss)
        
        # A correct prediction is to have the same maximum element
        self.correct_pred = tf.equal(tf.argmax(self.prediction, 2), tf.argmax(self.labels, 2))

        # Get the accuracy over the batch
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))

        # The saver
        self.saver = tf.train.Saver()

        # Initialize the variables
        self.init = tf.global_variables_initializer()

        # Start the tensorflow session
        self.sess = tf.Session()

        # Run the initializer (running now or else loading won't work)
        self.sess.run(self.init)

    def shuffle_data(self, data):
        # The data is a tuple of (image, action), shuffle it
        np.random.shuffle(data)

        return self.split_data(data)

    def split_data(self, data):
        # Split the tuples into 2 separate arrays
        split_in, split_out = np.hsplit(data, 2)

        # Stack and squeeze input to shape (batch_size, 128, 128, 1)
        split_in = np.stack(np.squeeze(split_in, 1), 0)

        # Stack and squeeze labels to shape (batch_size, 1, 20)
        split_out = np.stack(np.squeeze(split_out, 1), 0)

        return split_in, split_out

    def train(self, training_data, epochs):
        print("Training Starting\n")
        for epoch in range(epochs):
            # The average loss per epoch
            avg_loss = 0

            # The average accuracy per epoch
            avg_acc = 0

            # Shuffle to data every epoch to generalize it
            inps, labs = self.shuffle_data(training_data)

            for i in range(0, len(inps), self.batch_size):
                # Get the new batch
                batch_in = inps[i : i + self.batch_size, :, :, :]
                batch_out = labs[i : i + self.batch_size, :, :]

                _, loss, acc = self.sess.run([self.optimizer, self.loss,
                                              self.accuracy],
                                             feed_dict={self.inp:batch_in,
                                                        self.labels:batch_out})

                # There are inps / batch_size inputs so divided by it to get
                # average
                avg_loss += loss / (len(inps) / self.batch_size)
                avg_acc += acc / (len(inps) / self.batch_size)

            print("Epoch", str(epoch + 1) + ":", "Loss", avg_loss, "Accuracy", avg_acc)

        print("\nTraining complete\n")

    def test(self, test_data):
        print("Testing Starting\n")

        # Get the data, don't need to shuffle
        inps, labs = self.split_data(test_data)

        preds = []


        los, acc, pred = self.sess.run([self.loss, self.accuracy, self.prediction],
                                        feed_dict={self.inp:inps,
                                                   self.labels:labs})

        print("Loss:", los)
        print("Accuracy:", acc, "\n")
        print("Predictions                            - Labels\n")

        # Printing predictions may show badly for high losses
        for i in range(len(preds)):
            print(pred[i], "-", labs[i])

    def get_out(self, inpu):
        # Labels don't matter, only need the output
        labs = np.zeros((inpu.shape[0], 1, 20))

        return self.sess.run(self.prediction, feed_dict={self.inp:inpu,
                                                         self.labels:labs})
    
    def save(self, path):
        print("Saving model to", path, "\n")
        self.saver.save(self.sess, path)

    def load(self, path):
        print("Loading Model from", path, "\n")
        self.saver.restore(self.sess, path)
