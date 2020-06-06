import pandas as pd
import numpy as np
from utils.constants import BUY, SELL, DO_NOTHING


class Operation(object):
    """
    Class that represents a operation.

    """

    def __init__(self, id, close_price, invested_value, take_profit, stop_loss, position, initial_date):
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
        @param initial_date: initial date
        @@type initial_date: string
        @param final_date: final date
        @@type final_date: string
        """
        self._initial_price = close_price
        self._final_price = close_price
        self._result = None
        self._closed = False
        self._profit = 0
        self._position = position
        self._id = id
        self._initial_date = initial_date
        self._final_date = None

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
            if updated_price < (1 - self.take_profit) * self._initial_price or updated_price > (1 + self.stop_loss) * self._initial_price:
                self._final_price = updated_price
                return True
            else:
                return False

    def close(self, final_date):
        """
        Close operation.

        @return _profit: operation profit
        @@@type _profit: float
        @return history: operation profit
        @@@type history: dict
        """
        self._closed = True
        self._profit = self.get_profit()
        self._profit_percentage = self.get_profit_in_percentage()
        self._result = True if (self._final_price - self._initial_price) * self._position > 0 else False
        self._final_date = final_date

        history = {}
        history['Operation id'] = self._id
        history['Result'] = 'Success' if self._result else 'Fail'
        history['Entered as'] = 'BUY' if self._position == 1.0 else 'SELL'
        history['Profit (R$)'] = round(self._profit, 2)
        history['Profit (%)'] = f'{(self._profit_percentage * 100).round(2)} %'
        history['Invested value (R$)'] = self.invested_value
        history['Initial close price (R$)'] = self._initial_price
        history['Final close price (R$)'] = self._final_price
        history['Initial date'] = str(self._initial_date)
        history['Final date'] = str(self._final_date)

        return self.invested_value, self._profit, history

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
    
    def get_cash_open(self):
        """
        Calculates total cash in activity

        @return: total cash
        @@@type: float
        """
        profit_percentage = self.get_profit_in_percentage()        
        return (1 + profit_percentage) * self.invested_value

    def get_profit_in_percentage(self):
        """
        Calculates operation profit
        
        @return: operation profit in percentage
        @@@type: float
        """
        return self._position * (self._final_price - self._initial_price) / self._initial_price
    
    def is_open_position(self):
        """
        Check if it is still open.

        @return _closed: operation status
        @@@type _closed: boolean
        """
        return not self._closed
