import yfinance as yf
import numpy as np
from pandas_datareader import data as pdr
from datetime import date
from tools.AbstractTool import AbstractTool

class BacktestTool(AbstractTool):
    """
    This class represents a tool for backtesting purposes.

    """
    yf.pdr_override()

    def __init__(self, symbols, initial_date, final_date):
        """
        Class constructor.

        @param symbols: symbols that should be used while backtesting
        @@type symbols: list of strings
        @param initial_date: initial date to get data
        @@type initial_date: datetime string in the format "%YYYY-%MM-%DD"
        @param final_date: final date to get data
        @@type final_date: datetime string in the format "%YYYY-%MM-%DD"
        """
        self.symbols = symbols
        self.data = None
        self.initial_date = initial_date
        self.final_date = final_date

    def execute(self, agent):
        """
        Runs the backtest tool.

        @param agent: the agent the method should be executed on.
        @@type agent: class Agent
        """
        data = self._get_data()
        
    def _get_data(self):
        """
        Method to get data online using yahoo finance api.

        @return data: data achieved online
        @@@type data: list of dataframes
        """
        if initial_date and final_date:
            # Initialize empty data
            self.data = np.array([])
            for symbol in self.symbols:
                # Get stock data from yahoo
                stock_data = pdr.get_data_yahoo(
                    symbol, start=self.initial_date, end=self.final_date)

                # Save it
                np.append(self.data, stock_data)

            return self.data

        elif not initial_date:
            raise ValueError("Initial date can't be an empty value.")

        else:
            raise ValueError("Final date can't be an empty value.")
