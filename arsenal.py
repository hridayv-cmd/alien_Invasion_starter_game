import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

# Avoid circular imports while allowing type hinting
if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class Arsenal:
    """Manages the ship's weapons, bullet limits, and screen cleanup."""
    def __init__(self, game: 'AlienInvasion'):
        """Initialize settings and create a group to store active bullets."""
        self.game = game
        self.settings = game.settings
        # Pygame sprite group to manage and update multiple bullets easily
        self.arsenal = pygame.sprite.Group()
    


    def update_arsenal(self) -> None:
        """Update bullet positions and clean up any that go off-screen."""
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self) -> None:
        """Delete off-screen bullets to save system memory and maintain performance."""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self) -> None:
        """Draw every active bullet on the screen."""
        for bullet in self.arsenal:
            bullet.draw_bullet()

    
    def fire_bullet(self):
        """Spawn a new bullet if the player has not hit the maximum bullet limit."""
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True #Successfully fired
        return False    # Limit reached, did not fire
