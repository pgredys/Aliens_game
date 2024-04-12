import pygame.font

from settings import Settings


class Scoreboard:
    """Class representing a scoreboard"""

    def __init__(self, ai_game):
        """Initialise the scoreboard"""

        self.score_rect = None
        self.store_image = None
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for information
        self.text_color = "#2b2b2b"
        self.font = pygame.font.SysFont(None, 48)

        # prepare initial score
        self.prep_score()

    def prep_score(self):
        """Prepare score for display"""
        # score in arcade style
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,}'

        self.store_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display
        self.score_rect = self.store_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Show score on the screen"""
        self.screen.blit(self.store_image, self.score_rect)
