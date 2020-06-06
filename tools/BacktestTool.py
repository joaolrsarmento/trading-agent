import yfinance as yf
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from tools.AbstractTool import AbstractTool
from utils.constants import BUY, SELL, DO_NOTHING


class BacktestTool(AbstractTool):
    """
    This class represents a tool for backtesting purposes.

    """
    yf.pdr_override()

    def __init__(self, initial_balance=1000.0,
                 symbol='AAPL',
                 initial_date="2019-01-01",
                 final_date="2020-01-01",
                 take_profit=0.03,
                 stop_loss=0.01):
        """
        Class constructor.

        @param initial_balance: initial_balance
        @@type initial_balance: float
        @param symbols: symbols that should be used while backtesting
        @@type symbols: list of strings
        @param initial_date: initial date to get data
        @@type initial_date: datetime string in the format "%YYYY-%MM-%DD"
        @param final_date: final date to get data
        @@type final_date: datetime string in the format "%YYYY-%MM-%DD"
        @param take_profit: take profit constant (where stop the operation for profit)
        @@type take_profit: float
        @param stop_loss: stop loss constant (where stop the operation for loss)
        @@type stop_loss
        """
        parameters = {
            "Initial balance": initial_balance,
            "Symbol": symbol,
            "Initial date": initial_date,
            "Final date": final_date
        }

        super().__init__(tool_name="Backtest", parameters=parameters)

        self.symbol = symbol
        self.data = None
        self.initial_date = initial_date
        self.final_date = final_date
        self.initial_balance = initial_balance

    def execute_agent(self, agent, save_log=True):
        """
        Runs the backtest tool.

        @param agent: the agent the method should be executed on.
        @@type agent: class Agent
        """
        print(f'Running backtest on agent {agent.get_name()}...')

        data = self.get_data()

        total_length = len(data)
        for i in range(1, total_length):
            agent.update(data[0:i])

        active_operation_data = agent.get_active_operation_data(
            data['Close'][-1])
        profit_data, operation_history = agent.get_history()
        balance = agent.get_balance()

        data = self._create_backtest_log_data(
            agent, active_operation_data, balance, profit_data, operation_history)

        # Save log file
        if save_log:
            self.log.log(data)

    def get_data(self):
        """
        Method to get data online using yahoo finance api.

        @return data: data achieved online
        @@@type data: list of dataframes
        """
        if self.initial_date and self.final_date:
            # Get stock data from yahoo
            self.data = pdr.get_data_yahoo(
                self.symbol, start=self.initial_date, end=self.final_date)

            self.data['Change'] = self.data['Close'].pct_change()

            return self.data

        elif not initial_date:
            raise ValueError("Initial date can't be an empty value.")

        else:
            raise ValueError("Final date can't be an empty value.")

    def _create_backtest_log_data(self, agent, active_operation_data, balance, profit_data, operation_history):
        """
        Method to create the data that goes into the log file.
        
        """
        # Initialize as empty
        data = {}
        # Get model name and tools parameters
        data['Used on'] = agent.get_name()
        data['Initial date'] = self.initial_date
        data['Final date'] = self.final_date
        data['Initial balance (R$)'] = self.initial_balance
        # Get the last values achieved
        data['Final balance (R$)'] = balance
        data['Final profit (R$)'] = profit_data[0]
        data['Final profit (%)'] = profit_data[1]
        data['Active operations (#)'] = active_operation_data[0]
        data['Active operations (R$)'] = active_operation_data[1]
        data['Operations history'] = operation_history

        return data

