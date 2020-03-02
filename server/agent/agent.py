from tensorflow.keras.models import load_model, Model
from tensorflow.keras import backend as K
import numpy as np

class Agent(object):

    def __init__(self, batch_size=8):
        self.batch_size = batch_size
        self.model = None
        pass

    def load_model(self, save_path):
        """
            Loads a saved compiled model.

        """
        if(self.model == None):
            self.model = load_model(save_path)
            return
        print("errs")
        return    

    def reset_model(self):
        """
            Resets the current model in memory.

        """
        if(self.model != None):
            self.model = None
