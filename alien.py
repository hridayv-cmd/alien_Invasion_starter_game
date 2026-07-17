import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    def __init__(self, fleet: 'AlienFleet', x: float, y:float ):
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings
        
        # Load and scale the alien image asset
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.alien_w, self.settings.alien_h) 
            )
        
        # Position the alien using the provided x and y coordinates
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Store precise decimal values for horizontal and vertical tracking
        self.y = float(self.rect.y)
        self.x = float(self.rect.x) 


    def update(self):
        """Move the alien right or left, dropping it down if it hits a wall."""
        temp_speed = self.settings.fleet_speed


        # Calculate new horizontal position based on direction and speed
        self.x += temp_speed * self.fleet.fleet_direction

        # Update actual rect coordinates
        self.rect.x = self.x
        self.rect.y = self.y


    
    def check_edges(self):
        """Return True if the alien's boundary rect touches the edge of the screen."""
        return (self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)


    def draw_alien(self):
        """Draw the alien onto the screen at its current position."""
        self.screen.blit(self.image, self.rect)