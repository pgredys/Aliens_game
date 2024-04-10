import sys
from random import randint
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from settings import Settings
from game_stats import GameStats
from ship import Ship


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
        pygame.display.set_icon(pygame.image.load('../assets/alien.bmp'))

        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = True

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
                self._create_alien(current_x, current_y) if randint(0, 10) >= 3 and self.settings.randomness \
                    else self._create_alien(current_x, current_y) if not self.settings.randomness else None

                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blit()
        self.aliens.draw(self.screen)

        if not self.game_active:
            sleep(2)
            sys.exit()

        pygame.display.flip()

    def _update_aliens(self):
        """Function to update the aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _change_fleet_direction(self):
        """Function to change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Function to check if any aliens have reached the edges"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """Update the bullets"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _fire_bullet(self):
        """Function to fire a bullet"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_bullet_alien_collisions(self):
        """Function to check if a bullet collides with the alien"""
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _ship_hit(self):
        """Function for alien-ship hit"""
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1

            self.bullets.empty()
            self.aliens.empty()

            # reset fleet and ship
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)

        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """Function to check if aliens have reached the bottom"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
