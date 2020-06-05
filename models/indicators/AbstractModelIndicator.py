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
        years = mdates.YearLocator()   # Every year
        months = mdates.MonthLocator()  # Every month
        days = mdates.DayLocator() # Every day

        format_date = mdates.DateFormatter('%b\n%Y') # Show month to month data

        fig, ax = plt.subplots()

        # Plot every single column in the dataframe
        x_axis = self.signals.index
        for column in self.signals.columns:
            if column not in exclude_columns:
                ax.plot(x_axis, self.signals[column])
        
        # Format the ticks
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(format_date)
        ax.xaxis.set_minor_locator(months)

        # Format the coords message box
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.grid(True)

        # Rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()

        # Set ylabel
        plt.legend([column for column in self.signals.columns if column not in exclude_columns])
        plt.show()

    def get_signals(self):
        """
        Method to get signals from a model.

        """
        raise NotImplementedError(
            "This class is abstract and should not have this method.")
