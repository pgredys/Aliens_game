import sys

import pygame
from settings import Settings
from alien import Alien

from random import randint


class AlienInvasion:
    """Class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_alien(self, position_x, position_y):
        """Create an alien group and add it to the row"""
        new_alien = Alien(self)
        new_alien.x = position_x
        new_alien.rect.x = position_x
        new_alien.rect.y = position_y
        self.aliens.add(new_alien)

    def _create_fleet(self):
        """Function to create fleet of aliens"""
        alien = Alien(self)
        self.aliens.add(alien)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < self.settings.screen_height - 3 * alien_height:
            while current_x < self.settings.screen_width - 2 * alien.rect.width:
                self._create_alien(current_x, current_y) if randint(0, 10) >= 3 else None
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.aliens.draw(self.screen)

        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._update_screen()
            self.clock.tick(60)


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()