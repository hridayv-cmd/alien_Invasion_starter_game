import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
#from alien import Alien
from alien_fleet import AlienFleet

class AlienInvasion: 
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()

        # Set up the display window using settings dimensions
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
            )
        pygame.display.set_caption(self.settings.name)

        # Load and scale the background image to fit the screen
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg,
            (self.settings.screen_w, self.settings.screen_h)
            )
        
        # Flag to manage the game state loop and set frame rate clock
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        # Initialize the ship and equip it with the weapon arsenal and add Alien
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()


    def run_game(self):
        """Start the main game loop to continuously update and redraw."""
        #Game loop
        while self.running:
            self._check_events()        # Look for player inputs (keys)
            self.ship.update()          # Calculate ship movement
            self.alien_fleet.update_fleet()         # Update the position and movement of the alien(s)
            self._check_collisions()      
            self._update_screen()       # Render everything onto the screen
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        #check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._reset_level()
           #subtract one life is possible

      

        

    def _reset_level(self):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()



    def _update_screen(self):
        """Redraw all game objects and refresh the display screen."""
        self.screen.blit(self.bg,(0,0))   # Draw background
        self.ship.draw()                  # Draw Ship
        self.alien_fleet.draw()           # Draw Alien
        self.ship.arsenal.draw()          # Show any active lasers
        pygame.display.flip()             # Show the newly drawn frame

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keyup_event(self, event) -> None:
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_event(self, event) -> None:
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)

        elif event.key == pygame.K_q:
           self.running = False
           pygame.quit()
           sys.exit()

if __name__ == '__main__':

    ai = AlienInvasion()
    ai.run_game()
