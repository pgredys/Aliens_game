from enum import Enum


class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game settings"""

        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.MODE = Mode(1)
        self.bg_color = self.MODE.bg_color()

        # Game settings
        self.randomness = True

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.alien_points = 50
        self.lasers_allowed = 3
        self.laser_color = (255, 0, 0)

        # fleet_direction: 1 -> right, -1 -> left
        self.fleet_direction = 1

        # Ship settings.
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = self.MODE.bullet_color()
        self.bullets_allowed = 3

        # Ships per game
        self.ships_limit = 3

        # Dynamic alien speed
        self.speedup_scale = 1.1

        # score scale
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change aliens speed during game play"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def change_mode(self):
        self.MODE = next(self.MODE)
        self.bg_color = self.MODE.bg_color()
        self.bullet_color = self.MODE.bullet_color()


class Mode(Enum):
    LIGHT = 0
    DARK = 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __next__(self):
        if self.value != len(Mode) - 1:
            return Mode(self.value + 1)
        else:
            return Mode(0)

    def bg_color(self):
        if self == Mode.LIGHT:
            return '#ffffff'
        if self == Mode.DARK:
            return '#2b2b2b'

    def bullet_color(self):
        if self == Mode.LIGHT:
            return '#000000'
        if self == Mode.DARK:
            return '#505050'

    def button_color(self):
        if self == Mode.LIGHT:
            return '#44FF00'
        if self == Mode.DARK:
            return '#227900'
