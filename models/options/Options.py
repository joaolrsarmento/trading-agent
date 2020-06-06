from enum import Enum

class Options(Enum):
    """
    Possible actions to take:
    - Do nothing
    - Buy a share
    - Sell a share
    
    """
    DO_NOTHING = 0.0
    BUY = 1.0
    SELL = -1.0
