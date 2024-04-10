from settings import Settings


class GameStats:
    """Track stats for Aliens Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.ships_left = None
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Reset stats"""
        self.ships_left = self.settings.ships_limit

