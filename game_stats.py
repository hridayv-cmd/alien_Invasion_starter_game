class GameStats():
    """Track global runtime statistics and active life balances for the game."""
    
    def __init__(self, ship_limit):
        """Initialize running state metrics and resource tracking allocations."""
        
        # Total remaining player life counts allowed before game-over state
        self.ship_left = ship_limit

        

    