import pandas as pd
import numpy as np
from tools.BacktestTool import BacktestTool
from agent.options import Options


class AbstractAgent(object):
    """
    Abstract class to represent a agent.

    """

    def __init__(self, agent=None, agent_name="Random Agent"):
        self.agent_name = agent_name
        self.agent = agent

    def run_backtest(self, initial_balance=1000, initial_date="2010-01-01", final_date="2019-01-01", symbol="AAPL"):
        backtest = BacktestTool(symbol)
        data = backtest.get_data()

        data['Signal'] = data['Close']
