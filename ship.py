import pygame
from typing import TYPE_CHECKING

# Avoid circular imports while allowing type hinting
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    """Manages player ship behavior, movement, rendering, and firing."""

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """Initialize the ship and set its starting position at bottom-center."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        # Load and scale the player ship image
        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image,
            (self.settings.ship_w, self.settings.ship_h) 
            )
        
        # Initialize placement properties
        self.rect = self.image.get_rect()
        self._center_ship()

        # Movement flags to track ongoing key presses
        self.moving_right = False
        self.moving_left  = False
        self.arsenal = arsenal

    def _center_ship(self):
        """Reset the ship back to its starting bottom-center coordinate position."""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)     # Track precise decimal position for horizontal tracking

    def update(self):
        """Update the ship's position and manage weapon cooling/updates."""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """Adjust the ship's horizontal position while keeping it in screen boundaries."""
        temp_speed = self.settings.ship_speed
        
        # Move right if flag is active and ship hasn't hit the right boundary
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed

            # Move left if flag is active and ship hasn't hit the left boundary
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed

        # Sync the structural layout rect position with the floating mathematical variable
        self.rect.x = self.x


    def draw(self) -> None:
        """Draw the ship on screen at its current position."""
        self.screen.blit(self.image, self.rect )


    def fire(self):
        """Request the weapon arsenal to fire a bullet."""
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group):
        """Detect individual contact hits with elements like the alien fleet group."""
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()     # Snap back to center upon taking damage
            return True
        return False
    