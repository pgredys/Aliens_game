import random
from pathlib import Path

import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    """A class to represent a bullet."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.laser_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 2 * self.settings.bullet_height)
        alien = random.choice(list(ai_game.aliens))
        self.rect.midbottom = alien.rect.midbottom

        self.y = float(self.rect.y)
        self.direction = 1

        self.fire_sound = pygame.mixer.Sound(Path('../assets/audio/laser.wav'))
        pygame.mixer.Sound.play(self.fire_sound).set_volume(.3)

    def update(self):
        """Move the bullet forward"""
        self.y += self.direction * .5 * self.settings.bullet_speed
        self.rect.y = self.y

    def draw_laser(self):
        """Draw the bullet"""
        pygame.draw.rect(self.screen, self.color, self.rect)
