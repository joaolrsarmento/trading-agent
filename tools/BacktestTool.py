import yfinance as yf
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from tools.AbstractTool import AbstractTool
from models.Options import Options
from utils.constants import BUY, SELL, DO_NOTHING

class BacktestTool(AbstractTool):
    """
    This class represents a tool for backtesting purposes.

    """
    yf.pdr_override()

    def __init__(self, initial_balance=1000.0, symbol='AAPL', initial_date="2019-01-01", final_date="2020-01-01"):
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

    def execute_agent(self, agent, save_log=True, plot_signals=False, plot_backtest_data=True):
        """
        Runs the backtest tool.

        @param agent: the agent the method should be executed on.
        @@type agent: class Agent
        """
        print(f'Running backtest on agent {agent.get_name()}...')

        data = self.get_data()
        agent.update(data)
        signals = agent.get_signals()
        generated_data = self._generate_backtest_data(signals, data)

        # Plot the data generated (only percentage profit is now been plotted)        
        if plot_backtest_data:
            self._plot_backtest_data(agent, generated_data)

        # Plot model signals
        if plot_signals:
            agent.plot()

        # Save log file
        if save_log:
            data = self._create_backtest_log_data_for_model(agent, generated_data)
            self.log.log(data)

        
    def execute_model(self, model, save_log=True, plot_signals=False, plot_backtest_data=True):
        """
        Runs the backtest tool.

        @param model: the model the method should be executed on.
        @@type agent: class derived from models.AbstractModel class
        """
        print(f'Running backtest on model {model.get_name()}...')

        data = self.get_data()
        model.update(data)
        signals = model.get_signals()
        generated_data = self._generate_backtest_data(signals, data)

        # Plot the data generated (only percentage profit is now been plotted)        
        if plot_backtest_data:
            self._plot_backtest_data(model, generated_data)

        # Plot model signals
        if plot_signals:
            model.plot()

        # Save log file
        if save_log:
            data = self._create_backtest_log_data_for_model(model, generated_data)
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
    
    def _create_backtest_log_data_for_model(self, object_used, generated_data):
        """
        Method to create the data that goes into the log file.

        @param model: model that is been used for this tool
        @@type model: a class derived from models.AbstractModel class
        @param generated_data: the data that was generated using this tool
        @@type generated_data: pandas DataFrame
        
        @return data: the generated data
        @@@type data: dict
        """
        # Initialize as empty
        data = {}
        # Get model name and tools parameters
        data['Used on'] = object_used.get_name()
        data['Initial date'] = self.initial_date
        data['Final date'] = self.final_date
        data['Initial balance (R$)'] = self.initial_balance 
        # Get the last values achieved
        data['Final balance (R$)'] = generated_data['Balance'][-1]
        data['Final profit (R$)'] = generated_data['Profit'][-1]
        data['Final profit (%)'] = generated_data['Profit %'][-1]
        # Count operations
        data['Total buy operations'] = int((generated_data['Options'] == BUY).sum())
        data['Total sell operations'] = int((generated_data['Options'] == SELL).sum())
        data['Total operations'] = data['Total buy operations'] + data['Total sell operations']
        # Get total history
        data['History'] = generated_data.to_dict(orient='index')

        return data
    def _plot_backtest_data(self, model, generated_data):
        """
        Method plot % profit calculated by the tool.

        @param model: model that is been used for this tool
        @@type model: a class derived from models.AbstractModel class
        @param generated_data: the data that was generated using this tool
        @@type generated_data: pandas DataFrame
        """
        print('Plotting backtest data...')

        fig, ax = plt.subplots()

        ax.plot(generated_data.index, generated_data['Profit %'])

        plt.ylabel('Profit (%)')
        plt.xlabel('Date')
        plt.show()

    def _generate_backtest_data(self, signals, data):
        """
        Method to generate the main data.

        @param signals: signals obtained using the model
        @@type signals: pandas DataFrame

        @return generated_data: generated data
        @@@type generated_data: pandas DataFrame
        """
        # Create the DataFrame using the same index as signals
        generated_data = pd.DataFrame(index=signals.index)
        # Calculate the updated values at each index 
        generated_data['Balance'] = (
            (1 + signals['Signal'] * data['Change'].shift(1)).cumprod()) * self.initial_balance
        generated_data['Profit'] = (
            generated_data['Balance'] - self.initial_balance)
        generated_data['Profit %'] = (
            generated_data['Balance'] / self.initial_balance - 1) * 100
        # Saves the options used
        generated_data['Options'] = signals['Signal']
        # Avoid erros
        generated_data.fillna(0, inplace=True)
        # Format index
        generated_data.index = generated_data.index.strftime("%Y-%m-%d")

        return generated_data
