import pandas as pd
import numpy as np
from utils.constants import BUY, SELL, DO_NOTHING


class Operation(object):
    def __init__(self, close_price, invested_value, take_profit, stop_loss, position):
        self._initial_price = close_price
        self._final_price = close_price
        self._operation_result = None
        self._operation_closed = False
        self._profit = 0
        self._position = position

        self.invested_value = invested_value
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def reached_endpoint(self, updated_price):
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
        self._operation_closed = True
        self._profit = self.get_profit()

        if self._final_price > self._initial_price:
            self._operation_result = True
        else:
            self._operation_result = False

        return self._profit

    def get_final_price(self):
        return self._final_price

    def get_initial_price(self):
        return self._initial_price

    def get_profit(self):
        return self.invested_value * self._position * (self._final_price - self._initial_price) / self._initial_price

    def is_open_position(self):
        return not self._operation_closed
