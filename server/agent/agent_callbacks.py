import tensorflow as tf
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import scipy.misc
from random import randint
cwd = os.getcwd()


class Autoencoder_Callbacks(tf.keras.callbacks.Callback):

    def __init__(self, val_data):
        super().__init__()
        self.validation_data = val_data

    def on_train_begin(self, logs=None):
        return

    def on_train_end(self, logs=None):
        return

    def on_epoch_begin(self, epoch, logs=None):
        # print(np.shape(self.validation_data[0][0]))
        return

    def on_epoch_end(self, epoch, logs=None):
        return

    def on_batch_begin(self, batch, logs=None):
        return

    def on_batch_end(self, batch, logs=None):
        return


