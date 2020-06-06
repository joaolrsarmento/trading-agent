import pandas as pd
import numpy as np
from models.operations.Operation import Operation
from models.indicators.SimpleMovingAverageCrossover import SimpleMovingAverageCrossover
from models.AbstractModel import AbstractModel
from utils.constants import BUY, SELL, DO_NOTHING

class AbstractAgent(object):
    """
    This class represents an abstract agent.

    """

    def __init__(self, agent_name="Abstract Agent", balance=10000, percentage=0.1, take_profit=0.03, stop_loss=0.01):
        """
        Class constructor.

        @param agent_name: agent name
        @@type agent_name: string
        """
        self.agent_name = agent_name
        self.models = []
        self.signals = pd.DataFrame()
        self.operations = []
        self.balance = balance
        self.active_balance_percentage = percentage
        self.take_profit = take_profit
        self.stop_loss = stop_loss

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
        self.signals['Close'] = data['Close']
        self.signals['Signal'] = signals
        # Check for operations update
        self._update_operations(data)

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

    def _should_create_operation(self, signals):
        """
        Check if should create a new operation based on last signal.

        @param signals: all the signals until this moment.
        @@type signals: pandas dataframe

        @return boolean that represents the operation creation
        """
        if signals['Signal'][-1] in [BUY, SELL]:
            return True

        return False

    def _update_operations(self, data):
        """
        Go through all operation to check if any should be closed. Also, check for operation creation

        @param data: data updated
        @@type data: pandas dataframe
        """
        # Check for operation creation
        if self._should_create_operation(self.signals):
            # Get last position
            position = self.signals['Signal'][-1]
            # Create
            self._create_operation(self.signals, position)

        # Check for operation closing
        for operation in self.operations:
            # If it is still open
            if operation.is_open_position():
                # Check for endpoint
                if operation.reached_endpoint(data['Close'][-1]):
                    # Store operation data
                    operation_id, operation_result, operation_profit = operation.close()
    
    def _create_operation(self, signals, position):
        """
        Creates a new operation. For now, its only theoretical.

        @param signals: updated signals
        @@type signals: pandas dataframe
        @param position: position the operation should run on
        @@type position: BUY or SELL constant
        """

        # Create operation
        operation = Operation(id=len(self.operations),
                              close_price=signals['Close'][-1],
                              invested_value=self.balance * self.active_balance_percentage,
                              take_profit=self.take_profit,
                              stop_loss=self.stop_loss,
                              position=position)
        # Save it
        self.operations.append(operation)
        