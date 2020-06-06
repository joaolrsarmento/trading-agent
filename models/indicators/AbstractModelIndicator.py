import pandas as pd
import numpy as np
from models.AbstractModel import AbstractModel
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
import matplotlib


class AbstractModelIndicator(AbstractModel):
    """
    This class represents a abstract model indicator.

    """

    def __init__(self, model_name="Abstract Model"):
        """
        Class constructor.

        """
        super().__init__(model_name=model_name)
        self.signals = None

    def plot(self, exclude_columns=[]):
        """
        Plotting signals obtained.

        """
        # Check for errors
        if np.all(self.signals, None):
            raise ValueError("Signals haven't been generated yet.")
        
        print(f'Plotting signals from {self.get_name()}...')

        fig, ax = plt.subplots()

        for column in self.signals.columns:
            if column not in exclude_columns:
                ax.plot(self.signals.index, self.signals[column])

        # Set ylabel
        plt.legend([column for column in self.signals.columns if column not in exclude_columns])
        plt.show()

    def get_signals(self):
        """
        Method to get signals from a model.

        """
        if np.all(self.signals == None):
            raise ValueError("Signals haven't been generated yet.")

        return self.signals
