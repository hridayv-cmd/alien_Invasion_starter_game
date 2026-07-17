import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
#from alien import Alien
from alien_fleet import AlienFleet
from time import sleep


class AlienInvasion: 
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.game_stats = GameStats(self.settings.starting_ship_count)

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
        self.game_active = True


    def run_game(self):
        """Start the main game loop to continuously update and redraw."""
        #Game loop
        while self.running:
            self._check_events()  # Look for player inputs (keys)
            if self.game_active: 
                self.ship.update()          # Calculate ship movement
                self.alien_fleet.update_fleet()         # Update the position and movement of the alien(s)
                self._check_collisions()      
            self._update_screen()       # Render everything onto the screen
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        #check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
           #subtract one life is possible
        
        #check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()

        # check collisions of projectiles and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)


        if self.alien_fleet.check_destroy_status():
            self._reset_level()
            
        

      
    def _check_game_status(self):

        if self.game_stats.ship_left > 0:
            self.game_stats.ship_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False

      
        

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
