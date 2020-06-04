import pandas as pd
import numpy as np
from models.Options import Options


class AbstractModel(object):
    """
    Abstract class to represent a model.

    """

    def __init__(self, model_name="Random Model"):
        """
        Agent constructor.

        @param model_name: model name
        @@type model_name: string
        """
        self.model_name = model_name


    def run_tool(self, tool):
        """
        Method to run backtest on specific symbols using the same model.
        
        @param tool: tool to be executed
        @@type tool: a class derived from tools.AbstractTool class
        """
        tool.execute()
        
    def get_signals(self, data = None):
        """
        Method to get signals from a model.

        @param data: empty
        @@type data: None
        """
        raise NotImplementedError("This class is abstract and should not have this method.")

