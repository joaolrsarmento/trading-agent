import pandas as pd
from models.AbstractModel import AbstractModel
from matplotlib import pyplot as plt

class AbstractModelIndicator(AbstractModel):
    """
    This class represents a abstract model indicator.

    """
    def __init__(self, model_name="Abstract Model"):
        """
        Class constructor.

        """
        super.__init__(model_name=model_name)
        self.signals = None

    def plot(self):
        """
        Plotting signals obtained.

        """
        # Check for errors
        if not self.signals:
            raise ValueError("Signals haven't been generated yet.")

        # Plot every single column in the dataframe
        x_axis = self.signals.index
        for column in self.signals.columns:
            plt.plot(x_axis, self.signals[column])
        
        plt.show()

    def get_signals(self):
        """
        Method to get signals from a model.

        """
        raise NotImplementedError("This class is abstract and should not have this method.")

