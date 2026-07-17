import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

# Avoid circular imports while allowing type hinting
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Bullet(Sprite):
    """A class to manage laser bullets fired from the player's ship."""
    def __init__(self, game: 'AlienInvasion'):
        """Initialize the bullet sprite and set its starting position."""
        super().__init__()
        
        self.screen = game.screen
        self.settings = game.settings

        # Load the bullet graphic and scale it to the size specified in settings
        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.bullet_w, self.settings.bullet_h) 
            )
        
        # Position the bullet at the top-middle of the ship
        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.rect.y -= 50
        # Store a decimal value for precise vertical movement tracking
        self.y = float(self.rect.y)


    def update(self):
        """Move the bullet vertically up the screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet image on the screen at its current position."""
        self.screen.blit(self.image, self.rect)