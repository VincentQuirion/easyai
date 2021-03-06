import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

from scipy import ndimage

""" Contains all the classes necessary for students to easily build a TensorFlow model """


class MNIST(tf.keras.models.Sequential):
    """ Sequential model to classify digits from the MNIST dataset """

    dataset = tf.keras.datasets.mnist
    default_neuron_amount = 128
    default_layer_amount = 1
    epochs = 5
    optimizer = 'adam'
    loss_function = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    def __init__(self, layer_amount=default_layer_amount, neuron_amount=default_neuron_amount):
        # Create the model
        super().__init__()

        # Load the dataset
        (self.x_train, self.y_train), (self.x_test, self.y_test) = tf.keras.datasets.mnist.load_data()

        # Normalize the dataset's features
        self.x_train, x_test = self.x_train / 255.0, self.x_test / 255.0

        # Add the input layer
        self.add(tf.keras.layers.Flatten(input_shape=(28, 28)))

        # Add the amount of hidden layers chosen by the student
        for layer in range(layer_amount):
            self.add(tf.keras.layers.Dense(neuron_amount, activation='relu'))
            self.add(tf.keras.layers.Dropout(0.2))

        # Add the output layer
        self.add(tf.keras.layers.Dense(10))

        # Compile the model
        self.compile(optimizer=self.optimizer, loss=self.loss_function, metrics=['accuracy'])

    # Train the model
    def train(self, epochs=epochs):
        self.fit(self.x_train, self.y_train, epochs=epochs, validation_data=(self.x_test, self.y_test))

    # Return the model's prediction for an input
    def predict(self, x):
        # Make the array (x, 28, 28) even if the input is only (28, 28) --> i.e. to predict only one datapoint
        if len(x.shape) < 3:
            x = np.array([x])

        # Return the model's prediction as a vector
        prediction = super().predict(x)

        # Convert the vector into probabilities
        prediction = tf.nn.softmax(prediction).numpy()

        # Convert the probabilities into a final answer and return it
        return np.argmax(prediction)


    @staticmethod
    def preprocess_input(filepath):
        """
        Code is from https://medium.com/@o.kroeger/tensorflow-mnist-and-your-own-handwritten-digits-4d1cd32bbab4
        """

        # Read the image
        gray = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

        # Resize the images and invert it (black background)
        #gray = cv2.resize(255 - gray, (28, 28))

        flatten = gray.flatten() / 255.0

        (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        gray = cv2.resize(255 - gray, (28, 28))

        while np.sum(gray[0]) == 0:
            gray = gray[1:]

        while np.sum(gray[:, 0]) == 0:
            gray = np.delete(gray, 0, 1)

        while np.sum(gray[-1]) == 0:
            gray = gray[:-1]

        while np.sum(gray[:, -1]) == 0:
            gray = np.delete(gray, -1, 1)

        rows, cols = gray.shape

        if rows > cols:
            factor = 20.0 / rows
            rows = 20
            cols = int(round(cols * factor))
            gray = cv2.resize(gray, (cols, rows))
        else:
            factor = 20.0 / cols
            cols = 20
            rows = int(round(rows * factor))
            gray = cv2.resize(gray, (cols, rows))

        colsPadding = (int(math.ceil((28 - cols) / 2.0)), int(math.floor((28 - cols) / 2.0)))
        rowsPadding = (int(math.ceil((28 - rows) / 2.0)), int(math.floor((28 - rows) / 2.0)))
        gray = np.lib.pad(gray, (rowsPadding, colsPadding), 'constant')

        def getBestShift(img):
            cy, cx = ndimage.measurements.center_of_mass(img)

            rows, cols = img.shape
            shiftx = np.round(cols / 2.0 - cx).astype(int)
            shifty = np.round(rows / 2.0 - cy).astype(int)

            return shiftx, shifty

        def shift(img, sx, sy):
            rows, cols = img.shape
            M = np.float32([[1, 0, sx], [0, 1, sy]])
            shifted = cv2.warpAffine(img, M, (cols, rows))
            return shifted

        gray = np.lib.pad(gray, (rowsPadding, colsPadding), "constant")

        shiftx, shifty = getBestShift(gray)
        shifted = shift(gray, shiftx, shifty)
        gray = shifted

        gray = cv2.resize(255 - gray, (28, 28))

        gray = np.invert(gray)

        return gray

    @staticmethod
    def show_input(x):
        plt.imshow(x, cmap=plt.cm.binary)
        plt.show()



