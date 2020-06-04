from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
import numpy as np

yf.pdr_override()


class BacktestTool(object):
    """
    This class represents a tool for backtesting purposes.

    """

    def __init__(self, symbols):
        """
        Class constructor.

        @param symbols: symbols that shall be used to backtest
        @@type symbols: list of strings
        """
        self.symbols = symbols
        self.data = None

    def get_data(self, initial_date=None, final_date=None):
        """
        Method to get data online using yahoo finance api.

        @param initial_date: initial date to get data
        @@type initial_date: datetime string in the format "%YYYY-%MM-%DD"
        @param final_date: final date to get data
        @@type final_date: datetime string in the format "%YYYY-%MM-%DD"

        @return data: data achieved online
        @@@type data: list of dataframes
        """
        if initial_date and final_date:
            # Initialize empty data
            self.data = np.array([])
            for symbol in self.symbols:
                # Get stock data from yahoo
                stock_data = pdr.get_data_yahoo(
                    symbol, start=initial_date, end=final_date)

                # Save it
                np.append(self.data, stock_data)

            return self.data

        elif not initial_date:
            raise ValueError("Initial date can't be an empty value.")

        else:
            raise ValueError("Final date can't be an empty value.")
