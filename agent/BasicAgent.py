import pandas as pd
import numpy as np
from models.indicators.SimpleMovingAverageCrossover import SimpleMovingAverageCrossover

class BasicAgent(object):
    """
    This class represents a basic trading bot.
    
    """
    def __init__(self, agent_name="Basic Agent"):
        self.agent_name = agent_name
        self.model = SimpleMovingAverageCrossover()