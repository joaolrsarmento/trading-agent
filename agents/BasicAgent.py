from agents.AbstractAgent import AbstractAgent
from models.indicators.SimpleMovingAverageCrossover import SimpleMovingAverageCrossover

class BasicAgent(AbstractAgent):
    """
    Agent for trading that contains SimpleMovingAverageCrossover model

    """
    def __init__(self):
        """
        Class constructor.

        """
        super().__init__('Basic Agent')
        self.create_agent()

    def create_agent(self):
        """
        Properly create the agent, adding its models and parameters.

        """
        self.add_model(SimpleMovingAverageCrossover())

    

