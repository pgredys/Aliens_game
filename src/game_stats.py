from settings import Settings


class GameStats:
    """Track stats for Aliens Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.level = None
        self.score = None
        self.ships_left = None
        self.settings = ai_game.settings
        self.reset_stats()
        
        self.high_score = 0

    def reset_stats(self):
        """Reset stats"""
        self.ships_left = self.settings.ships_limit
        
        self.score = 0
        self.level = 1

