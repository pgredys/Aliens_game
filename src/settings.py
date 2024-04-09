class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # Game settings
        self. randomness = True

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction: 1 -> right, -1 -> left
        self.fleet_direction = 1
