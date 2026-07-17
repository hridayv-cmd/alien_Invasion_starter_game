import pygame 
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    


class AlienFleet:
    """Manages the creation, movement, and drawing of the alien fleet."""
    
    def __init__(self, game: 'AlienInvasion'):
        """Initialize the fleet, link settings, and create the grid of aliens."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen

        # Pygame group to hold all alien sprites
        self.fleet = pygame.sprite.Group()
        
        # Load fleet movement settings
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        # Build the fleet
        self.create_fleet()

    def create_fleet(self):
        """Calculate spacing and spawn a row of aliens across the screen."""
        alien_w = self.settings.alien_w
        screen_w = self.settings.screen_w

        # Determine how many aliens fit on the screen
        fleet_w = self.calculate_fleet_size(alien_w, screen_w)

        # half_screen = self.settings.screen_w
        
        # Center the fleet horizontally on the screen
        fleet_horizontal_space = fleet_w * alien_w
        x_offset = int((screen_w-fleet_horizontal_space)//2)

        # Spawn each alien in its calculated position
        for col in range(fleet_w):
            current_x = alien_w * col + x_offset
            if col % 2 == 0:
                continue
            self._create_alien(current_x, 10)



    def calculate_fleet_size(self, alien_w, screen_w):
        """Calculate the max number of aliens that fit in a row with spacing."""
        fleet_w = (screen_w//alien_w)

        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        return fleet_w
    

    def _create_alien(self, current_x: int, current_y: int):
        """Create an individual alien and add it to the fleet group."""
        # Pass self.game instead of self so the Alien has access to the main game
        new_alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    
    def draw(self):
        """Draw every alien in the fleet onto the screen."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()
    
