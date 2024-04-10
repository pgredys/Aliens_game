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
