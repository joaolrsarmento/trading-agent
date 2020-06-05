import pandas as pd
import numpy as np
from models.Options import Options


class AbstractModel(object):
    """
    Abstract class to represent a model.

    """

    def __init__(self, model_name="Abstract Model"):
        """
        Agent constructor.

        @param model_name: model name
        @@type model_name: string
        """
        self._model_name = model_name
        self.signals = None
    
    def run_tool(self, tool, save_log=True, plot_signals=False, plot_tool_data=True):
        """
        Method to run backtest on specific symbols using the same model.
        
        @param tool: tool to be executed
        @@type tool: a class derived from tools.AbstractTool class
        """
        tool.execute_model(self, save_log, plot_signals, plot_tool_data)
        
    def get_signals(self):
        """
        Method to get signals from a model.

        """
        raise NotImplementedError("This class is abstract and should not have this method.")

    def get_name(self):
        """
        Get model name.
        
        """
        return self._model_name