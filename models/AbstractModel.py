import pandas as pd
import numpy as np
from tools.BacktestTool import BacktestTool
from models.options import Options


class AbstractModel(object):
    """
    Abstract class to represent a model.

    """

    def __init__(self, model_name="Random Model"):
        """
        Agent constructor.

        """
        self.model_name = model_name


    def run_backtest(self, agent = None, initial_balance=1000.00, initial_date="2010-01-01", final_date="2019-01-01", symbols=["AAPL"]):
        """
        Method to run backtest on specific symbols using the same model.

        @param agent: agent that the model is running on.
        @@type agent: class Agent
        @param initial_balance: value in the begin.
        @@type initial_balance: float
        @param initial_date: initial date to backtest
        @@type initial_date: string (datetime)
        @param final_date: final date to backtest
        @@type final_date: string (datetime)
        @param symbols: symbols that represents the shares to be tested at
        @@type symbols: list of strings

        @return history: history of trades
        @@@type history: list
        @return final_balance: values in the end
        @@@type final_balance: list
        """

        # Checking for error
        if not self.agent:
            raise NotImplementedError("Agent not implemented.")

        final_balance = np.array([] * len(symbols))
        history = np.array([] * len(symbols))

        backtest = BacktestTool(symbols)
        data = backtest.get_data(initial_date, final_date)

        data['Signal'] = self.agent.get_signals(data['Close'])

    def get_signals(self, data = None):
        """
        Abstract.

        @param data: empty
        @@type data: None
        """
        raise NotImplementedError("This class is abstract and should not have this method.")

