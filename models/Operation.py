import pandas as pd
import numpy as np
from utils.constants import BUY, SELL, DO_NOTHING


class Operation(object):
    """
    Class that represents a operation.

    """

    def __init__(self, id, close_price, invested_value, take_profit, stop_loss, position):
        """
        Class constructor.

        @param id: id for log purposes.
        @@type id: integer
        @param close_price: the close_price the operation went on
        @@type close_price: float
        @param invested_value: invested value on the operation
        @@type invested_value: float
        @param take_profit: profit stop constant
        @@type take_profit: float (is percentage)
        @param stop_loss: loss stop constant
        @@type stop_loss: float (is percentage)
        @param position: position the operation should run on
        @@type position: BUY or SELL
        """
        self._initial_price = close_price
        self._final_price = close_price
        self._result = None
        self._closed = False
        self._profit = 0
        self._position = position
        self._id = id

        self.invested_value = invested_value
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def reached_endpoint(self, updated_price):
        """
        Check for operation end.

        @param updated_price: updated close price
        @@type updated_price: float

        @return boolean that represents that if the operation should close
        """
        if self._position == BUY:
            if updated_price > (1 + self.take_profit) * self._initial_price or updated_price < (1 - self.stop_loss) * self._initial_price:
                self._final_price = updated_price
                return True
            else:
                return False
        else:
            if updated_price > (1 - self.take_profit) * self._initial_price or updated_price < (1 + self.stop_loss) * self._initial_price:
                self._final_price = updated_price
                return True
            else:
                return False

    def close(self):
        """
        Close operation.

        @return _id: operation id
        @@@type _id: integer
        @return _result: operation result
        @@@type _result: boolean
        @return _profit: operation profit
        @@@type _profit: operation profit
        """
        self._closed = True
        self._profit = self.get_profit()
        self._result = True if (self._final_price - self._initial_price) * self._position > 0 else False

        return self._id, self._result, self._profit

    def get_final_price(self):
        """
        Get final price.

        @return _final_price: final price
        """
        return self._final_price

    def get_initial_price(self):
        """
        Get initial price.

        @return _initial_price: final price
        """
        return self._initial_price

    def get_profit(self):
        """
        Calculates operation profit
        
        @return: operation profit
        @@@type: float
        """
        return self.invested_value * self._position * (self._final_price - self._initial_price) / self._initial_price

    def is_open_position(self):
        """
        Check if it is still open.

        @return _closed: operation status
        @@@type _closed: boolean
        """
        return not self._closed
