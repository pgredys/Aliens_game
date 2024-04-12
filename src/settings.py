class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game settings"""
        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (255, 255, 255)

        # Game settings
        self. randomness = True

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # fleet_direction: 1 -> right, -1 -> left
        self.fleet_direction = 1

        # Ship settings.
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 3

        # Ships per game
        self.ships_limit = 3

        # Dynamic alien speed
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change aliens speed during game play"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

