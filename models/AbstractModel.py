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


    def run_tool(self, tool):
        """
        Method to run backtest on specific symbols using the same model.

        """
        tool.execute()
        
    def get_signals(self, data = None):
        """
        Method to get signals from a model.

        @param data: empty
        @@type data: None
        """
        raise NotImplementedError("This class is abstract and should not have this method.")

