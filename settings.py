from pathlib import Path
class Settings:
    """A class to store all static configuration settings for the game."""

    def __init__(self) -> None:
        # Screen and display settings
        self.name: str = 'Alien Invasion'
        self.screen_w = 1200
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'

        # Player ship settings
        self.ship_file = Path.cwd() /'Assets' / 'images' / 'ship2.png'
        self.ship_w = 40
        self.ship_h = 60
        self.ship_speed = 5


        # Weapon and bullet settings
        self.bullet_file = Path.cwd() /'Assets' / 'images' / 'laserBlast.png'
        self.laser_sound = Path.cwd() /'Assets' / 'sound' / 'laser.mp3'
        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_amount = 5  # Max active bullets allowed on screen at once

        # Alien enemy settings
        self.alien_file = Path.cwd() / 'Assets' / 'Images' / 'enemy_4.png'
        self.alien_w = 40
        self.alien_h = 40
        self.fleet_speed = 2
        self.fleet_direction = 1        # 1 represents moving right; -1 represents moving left          
        self.fleet_drop_speed = 40      # How far down the screen the alien drops when hitting a wall