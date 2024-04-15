import pygame
from pygame.sprite import Sprite


class Live(Sprite):

    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load ship image
        self.image = pygame.image.load('../assets/imgs/heart.bmp')
        self.rect = self.image.get_rect()

        # store position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
