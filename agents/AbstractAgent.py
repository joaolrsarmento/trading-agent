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

    def __init__(self, agent_name="Abstract Agent", balance=10000, percentage=0.01, take_profit=0.03, stop_loss=0.01):
        """
        Class constructor.

        @param agent_name: agent name
        @@type agent_name: string
        """
        self._agent_name = agent_name
        self._history = []
        self._models = []
        self._signals = pd.DataFrame()
        self._operations = []
        self.initial_balance = balance
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
        self._models.append(model)
        # Create column
        self._signals[model.get_name()] = np.array([])
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
        for model in self._models:
            model.update(data)
            model_signals = model.get_signals()
            model_name = model.get_name()
            signals[model_name] = model_signals['Signal']

        # Save the signals from the agent for plotting purposes
        self._signals = signals
        signals = np.array([])
        # Iterate over dataframe rows for intersection checking
        for index, row in self._signals.iterrows():
            format_row = np.array(row)
            signals = np.append(signals, BUY if np.all(format_row == BUY)
                                else SELL if np.all(format_row == SELL) else DO_NOTHING)
        # Save it
        self._signals['Close'] = data['Close']
        self._signals['Signal'] = signals
        # Check for operations update
        self._update_operations(data)

    def run_tool(self, tool, save_log=True):
        """
        Method to run backtest on specific symbols using the same agent.

        @param tool: tool to be executed
        @@type tool: a class derived from tools.AbstractTool class
        """
        tool.execute_agent(self, save_log)

    def get_name(self):
        """
        Get agent name.

        """
        return self._agent_name

    def get_signals(self):
        """
        Get agent signals.

        """
        return self.signals

    def get_profit_data(self):
        """
        Get profit data.

        @return profit: total profit
        @@@type profit: float
        @return profit_percentage: profit in percentage
        @@@type profit_percentage: float
        """
        profit = self.balance - self.initial_balance
        profit_percentage = profit / self.initial_balance

        return profit, profit_percentage

    def get_history(self):
        """
        Get agent history.

        @return history: history
        @@@type history: list
        @return profit_data: profit and percentage profit
        @@@type profit_data: tuple
        """
        profit_data = self.get_profit_data()

        return profit_data, self._history

    def get_active_operation_data(self, updated_close_price):
        """
        Get the data available on active operations.

        """
        total_value_invested, total_operations_active = 0, 0

        for operation in self._operations:
            if operation.is_open_position():
                updated_value_invested = operation.get_cash_open()
                total_operations_active += 1
                total_value_invested += updated_value_invested
        
        return total_operations_active, total_value_invested

    def get_balance(self):
        """
        Get updated balance.

        @return: updated balance
        @@@type: float
        """
        return self.balance
        
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
        if self._should_create_operation(self._signals):
            # Get last position
            position = self._signals['Signal'][-1]
            # Create
            self._create_operation(self._signals, position)

        # Check for operation closing
        for operation in self._operations:
            # If it is still open
            if operation.is_open_position():
                # Check for endpoint
                if operation.reached_endpoint(data['Close'][-1]):
                    # Store operation data
                    invested_value, profit, operation_history = operation.close(data.index[-1])
                    self.balance += (profit + invested_value)
                    self._add_to_history(operation_history)

    def _create_operation(self, signals, position):
        """
        Creates a new operation. For now, its only theoretical.

        @param signals: updated signals
        @@type signals: pandas dataframe
        @param position: position the operation should run on
        @@type position: BUY or SELL constant
        """
        invested_value = round(self.balance * self.active_balance_percentage, 2)

        self.balance -= invested_value
        # Create operation
        operation = Operation(id=len(self._operations),
                              close_price=signals['Close'][-1],
                              invested_value=invested_value,
                              take_profit=self.take_profit,
                              stop_loss=self.stop_loss,
                              position=position,
                              initial_date=signals.index[-1])
        # Save it
        self._operations.append(operation)

    def _add_to_history(self, operation_history):
        self._history.append(operation_history)
