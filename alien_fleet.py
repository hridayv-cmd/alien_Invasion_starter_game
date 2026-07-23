import pygame 
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    


class AlienFleet:
    """Manages the creation, movement, boundary tracking, and drawing of the alien fleet."""
    
    def __init__(self, game: 'AlienInvasion'):
        """Initialize the fleet, link settings, and create the grid of aliens."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen

        # Pygame group to hold and update all alien sprites
        self.fleet = pygame.sprite.Group()

        # Load dynamic fleet movement configurations
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

      # Construct the initial grid of enemies
        self.create_fleet()

    def create_fleet(self):
        """Calculate alignment metrics and populate the screen with a grid of aliens."""
        # Define the structural variables from settings so they can be passed below
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        # Determine how many aliens fit on the screen grid and get placement offsets
        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)
        x_offset, y_offset = self.calculate_offsets(alien_w, alien_h, screen_w, fleet_w, fleet_h)
        
        # Build the final grouped fleet structure
        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        for row in range(fleet_h):
            for col in range(fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                # Create a checkered spacing effect by skipping even indexes
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_offsets(self, alien_w, alien_h, screen_w, fleet_w, fleet_h):
        """Calculate the top-left offset values required to perfectly center the fleet grid."""
        half_screen = self.settings.screen_h//2


        # Center the fleet horizontally and vertically on the screen
        fleet_horizontal_space = fleet_w * alien_w
        fleet_vertical_space = fleet_h * alien_h

        # Split remaining empty space evenly for margins
        x_offset = int((screen_w-fleet_horizontal_space)//2)
        y_offset = int((half_screen-fleet_vertical_space)//2)
        return x_offset,y_offset



    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """Determine maximum column and row capacities based on asset size metrics."""
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h /2)//alien_h)

        # Ensure grid widths balance properly on margins
        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2


        # Ensure grid heights balance properly on margins
        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2


    

        return int(fleet_w), int(fleet_h)
    

    def _create_alien(self, current_x: int, current_y: int):
        """Create an individual alien and add it to the fleet group."""
        # Pass self (the fleet) back to the alien, exactly like the original code
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """Scan fleet units to check if any have struck a screen edge boundary."""
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break


    def _drop_alien_fleet(self):
        """Shift every alien downwards on the Y-axis when an edge bounce triggers."""
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed


    def update_fleet(self):
        """Handle boundary evaluations and progress positional steps for all units."""
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """Render all alive fleet elements directly to the active surface display."""
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    
    def check_collisions(self, other_group):
        """Detect and process overlap hits between fleet members and lasers."""
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_bottom(self):
        """Evaluate if any fleet elements have reached or passed the player boundary line."""
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
    

    def check_destroy_status(self):
       """Return True if every single alien inside the group has been cleared."""
       return not self.fleet
