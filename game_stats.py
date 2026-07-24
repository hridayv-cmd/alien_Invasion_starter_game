from typing import TYPE_CHECKING

# Avoid circular imports while allowing type hinting
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats():
    """Track global runtime statistics and active life balances for the game."""
    
    def __init__(self, game: 'AlienInvasion'):
        """Initialize running state metrics and resource tracking allocations."""
        
        # Total remaining player life counts allowed before game-over state
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions):
        #Update score
        self._update_score(collisions)
        #Update max_score
        self._update_max_score()
         # update hi_score

    def _update_max_score(self):
        if self.score > self.max_score:
            self.max_score = self.score
        #print(f'Max: {self.max_score}')
   
    def _update_score(self, collisions):
        for alien in collisions.values():
            self.score += self.settings.alien_points
        #print(f'Basic: {self.score}')

    def update_level(self):
        self.level += 1
        #print(self.level)


    

        

    