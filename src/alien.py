import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ A class to manage the aliens """

    def __init__(self, ai_game):
        """ Initialize the alien and set its starting position """
        super().__init__()
        self.screen = ai_game.screen

        # load alien image and set rect attribute
        self.image = pygame.image.load('../assets/alien.bmp')
        self.rect = self.image.get_rect()

        # start each new alien on the top left side of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien possition
        self.x = float(self.rect.x)
