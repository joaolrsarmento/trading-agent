import pandas as pd
import numpy as np
from utils.constants import BUY, SELL, DO_NOTHING

class Operation(object):
    def __init__(self, close_price, invested_value, take_profit, stop_loss):
        self.initial_price = close_price
        self.final_price = close_price
        self.invested_value = invested_value
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.operation_result = None

    def reached_endpoint(self, updated_price):
        if updated_price > (1 + self.take_profit)* self.price:
            self.operation_result = True
            self.final_price = updated_price
            return True
        elif updated_price < (1 - self.stop_loss) * self.price:
            self.operation_result = False
            self.final_price = updated_price
            return True
        else:
            return False


