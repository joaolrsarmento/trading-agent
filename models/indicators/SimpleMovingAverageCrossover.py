import pandas as pd
import numpy as np
from models.indicators.AbstractModelIndicator import AbstractModelIndicator
from models.Options import Options


class SimpleMovingAverageCrossover(AbstractModelIndicator):
    """
    Model representing a moving average indicator.
    Basically, when the fast SMA crosses the slow SMA from the top, send a signal for long.
    When the fast SMA crosses the slow SMA from the bottom, send a signal for short.

    """

    def __init__(self, fast_factor=8, slow_factor=20):
        """
        Class constructor

        @param fast_factor: period of the faster SMA in number of candles
        @@type fast_factor: integer
        @param slow_factor: period of the slower SMA in number of candles
        @@type slow_factor: integer
        """
        super().__init__("Simple Moving Average Crossover")
        self.fast_factor = fast_factor
        self.slow_factor = slow_factor

    def update(self, data):
        """
        Update the data from the model.

        @param data: data used to generate the signals
        @@type data: pandas dataframe
        """
        signals = pd.DataFrame(index=data.index)
        signals['Close'] = data['Close']
        signals['Fast SMA'] = data['Close'].rolling(
            window=self.fast_factor).mean()
        signals['Slow SMA'] = data['Close'].rolling(
            window=self.slow_factor).mean()
        signals['Difference'] = np.where(
            signals['Fast SMA'] > signals['Slow SMA'], 1, 0)
        signals['Signal'] = signals['Difference'].diff()
        signals['Change'] = data['Close'].pct_change()
        signals.fillna(0, inplace=True)

        self.signals = signals
