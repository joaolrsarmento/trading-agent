from agents.AbstractAgent import AbstractAgent
from models.indicators.SimpleMovingAverageCrossover import SimpleMovingAverageCrossover

class BasicAgent(AbstractAgent):
    """
    Agent for trading that contains SimpleMovingAverageCrossover model

    """
    def __init__(self, balance=10000, percentage=0.1, take_profit=0.03, stop_loss=0.01):
        """
        Class constructor.

        """
        super().__init__('Basic Agent', balance=balance, percentage=0.1, take_profit=take_profit, stop_loss=stop_loss)
        
        self.create_agent()

    def create_agent(self):
        """
        Properly create the agent, adding its models and parameters.

        """
        self.add_model(SimpleMovingAverageCrossover(fast_factor=5, slow_factor=12))

    

