from pathlib import Path

import pygame
from pygame.sprite import Sprite

from utilities import image_transparent_bg


class Alien(Sprite):
    """ A class to manage the aliens """

    def __init__(self, ai_game):
        """ Initialize the alien and set its starting position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load alien image and set rect attribute
        self.image = pygame.image.load(image_transparent_bg('../assets/imgs/alien.bmp'))

        self.rect = self.image.get_rect()

        # start each new alien on the top left side of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien position
        self.x = float(self.rect.x)

        # load sounds
        self.crash_sound = pygame.mixer.Sound(Path('../assets/audio/alien_crash.wav'))
        self.crash_sound.set_volume(0.5)

    def check_edges(self):
        """ Check if alien is on screen edge """
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        """ Move the alien forward to the right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def make_crash_sound(self):
        pygame.mixer.Sound.play(self.crash_sound)
