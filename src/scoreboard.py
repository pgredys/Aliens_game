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
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """Prepare score for display"""
        # score in arcade style
        rounded_score = round(self.stats.score, -1)
        score_str = f'{rounded_score:,}'

        self.store_image = self.font.render(score_str, True, self.text_color)

        # Display
        self.score_rect = self.store_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Show score on the screen"""
        self.screen.blit(self.store_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def prep_high_score(self):
        """Prepare high score on the screen"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f'High Score: {high_score:,}'
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # Position
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.center = self.screen_rect.center
        self.high_score_rect.top = 20

    def check_high_score(self):
        """Check if there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Prepare level of display"""
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)

        # Position
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.bottom = self.screen_rect.bottom - 20
