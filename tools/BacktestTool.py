import yfinance as yf
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from tools.AbstractTool import AbstractTool
from utils.constants import BUY, SELL, DO_NOTHING
from tqdm import tqdm


class BacktestTool(AbstractTool):
    """
    This class represents a tool for backtesting purposes.

    """
    yf.pdr_override()

    def __init__(self,
                 symbol='AAPL',
                 initial_date="2019-01-01",
                 final_date="2020-01-01"
                 ):
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

        super().__init__(tool_name="Backtest")

        self.symbol = symbol
        self.data = None
        self.initial_date = initial_date
        self.final_date = final_date

    def execute_agent(self, agent, balance, percentage, take_profit, stop_loss, save_log=True):
        """
        Runs the backtest tool.

        @param agent: the agent the method should be executed on.
        @@type agent: class Agent
        """
        self.initial_balance = balance
        print(f'Running backtest on agent {agent.get_name()}...')

        data = self.get_data()

        total_length = len(data)
        for i in tqdm(range(1, total_length)):
            agent.update(data[0:i])


        active_operation_data = agent.get_active_operation_data(
            data['Close'][-1])
        operation_history = agent.get_history()
        balance = agent.get_balance()

        data = self._create_backtest_log_data(
            agent, active_operation_data, balance, operation_history)

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

    def _create_backtest_log_data(self, agent, active_operation_data, balance, operation_history):
        """
        Method to create the data that goes into the log file.

        """
        count_buy_operations, count_buy_success_operations, count_sell_operations, count_sell_success_operations, count_successful_operations, count_failed_operations = 0, 0, 0, 0, 0, 0

        for history in operation_history:
            if history['Entered as'].upper() == 'BUY':
                if history['Result'].upper() == 'SUCCESS':
                    count_buy_success_operations += 1
                count_buy_operations += 1
            else:
                if history['Result'].upper() == 'SUCCESS':
                    count_sell_success_operations += 1
                count_sell_operations += 1
            if history['Result'].upper() == 'SUCCESS':
                count_successful_operations += 1
            else:
                count_failed_operations += 1

        total_balance = balance + active_operation_data[1]
        initial_balance = self.initial_balance
        # Initialize as empty
        data = {}
        # Get model name and tools parameters
        data['Used on'] = agent.get_name()
        data['Symbol'] = self.symbol
        data['Initial date'] = self.initial_date
        data['Final date'] = self.final_date
        data['Balance'] = {
            'Initial (R$)': round(self.initial_balance, 2),
            'Final (R$)': round(total_balance, 2)
        }
        data['Profit'] = {
            'Total profit (R$)': round(total_balance - initial_balance, 2),
            'Total profit (%)': f'{((total_balance - initial_balance) / initial_balance * 100).round(2)} %'
        }
        data['Active'] = {
            'Total (#)': round(active_operation_data[0], 2),
            'Total (R$)': active_operation_data[1]
        }
        data['Operations'] = {
            'Total': count_buy_operations + count_sell_operations + active_operation_data[0],
            'Total closed': count_buy_operations + count_sell_operations,
            'Total buy closed': count_buy_operations,
            'Total buy closed successful': count_buy_success_operations,
            'Total sell closed': count_sell_operations,
            'Total sell closed successful': count_sell_success_operations,
            'Total successful': count_successful_operations,
            'Total failed': count_failed_operations,
            'History': operation_history
        }

        return data
