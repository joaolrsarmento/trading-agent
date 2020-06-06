import pandas as pd
import numpy as np
from models.indicators.SimpleMovingAverageCrossover import SimpleMovingAverageCrossover
from models.AbstractModel import AbstractModel
from utils.constants import BUY, SELL, DO_NOTHING

class AbstractAgent(object):
    """
    This class represents an abstract agent.

    """

    def __init__(self, agent_name="Abstract Agent"):
        """
        Class constructor.

        @param agent_name: agent name
        @@type agent_name: string
        """
        self.agent_name = agent_name
        self.models = []
        self.signals = pd.DataFrame()

    def add_model(self, model):
        """
        Add new model to the agent.

        @param model: model to be added.
        @@type model: class derived from models.AbstractModel class
        """
        # Append
        self.models.append(model)
        # Create column
        self.signals[model.get_name()] = np.array([])
        # Print
        print(f'Added model {model.get_name()}')

    def update(self, data):
        """
        Updated agent data. It's worth mentioning that we don't check for divergence on this agent.
        Basically, a BUY signal will be sent if all the signals from the models are BUY. The same for SELL.

        @param data: data used to generate the signals
        @@type data: pandas dataframe 
        """
        signals = pd.DataFrame(index=data.index)

        # Get all the signals
        for model in self.models:
            model.update(data)
            model_signals = model.get_signals()
            model_name = model.get_name()
            signals[model_name] = model_signals['Signal']

        # Save the signals from the agent for plotting purposes
        self.signals = signals
        signals = np.array([])
        # Iterate over dataframe rows for intersection checking
        for index, row in self.signals.iterrows():
            format_row = np.array(row)
            signals = np.append(signals, BUY if np.all(format_row == BUY)
                      else SELL if np.all(format_row == SELL) else DO_NOTHING)
        # Save it
        self.signals['Signal'] = signals

    def run_tool(self, tool, save_log=True, plot_signals=False, plot_tool_data=True):
        """
        Method to run backtest on specific symbols using the same agent.

        @param tool: tool to be executed
        @@type tool: a class derived from tools.AbstractTool class
        """
        tool.execute_agent(self, save_log, plot_signals, plot_tool_data)

    def get_name(self):
        """
        Get agent name.

        """
        return self.agent_name

    def get_signals(self):
        """
        Get agent signals.

        """
        return self.signals
