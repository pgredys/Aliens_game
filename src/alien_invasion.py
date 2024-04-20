import sys
from pathlib import Path
from random import randint
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from laser import Laser
from scoreboard import Scoreboard
from settings import Settings
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
        pygame.display.set_icon(pygame.image.load('../assets/imgs/icon.bmp'))

        pygame.mixer.init()
        pygame.mixer.music.load(Path('../assets/audio/music.wav'))
        pygame.mixer.music.play(-1)

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an active state.
        self.game_active = False

        # create buttons
        self.play_button = Button(self, "   Play   ", position='center')
        self.color_mode_button = Button(self, ' Color Mode ', position='bottom_left', size=21)

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
                self._create_alien(current_x, current_y) if randint(0, 10) >= 3 and self.settings.randomness else \
                    self._create_alien(current_x, current_y) if not self.settings.randomness else None

                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for lasers in self.lasers.sprites():
            lasers.draw_laser()

        self.ship.blit()

        self.aliens.draw(self.screen)
        self._fire_aliens_lasers()

        self.sb.show_score()

        if not self.game_active:
            pygame.mixer.music.stop()
            if self.stats.score > self.stats.high_score:
                self.stats.save_high_score()

            self.play_button.draw_button()
            self.color_mode_button.draw_button()

            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_play_button(self, mouse_pos):
        """Function to check for play button actions"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:
            pygame.mixer.music.play(-1)

            self.stats.reset_stats()

            self.game_active = True

            self.bullets.empty()
            self.lasers.empty()
            self.aliens.empty()

            self.settings.initialize_dynamic_settings()

            self.stats.level = 0

            self.sb.prep_images()

            pygame.mouse.set_visible(False)

    def _check_mode_button(self, mouse_pos):
        """Function to check for mode button actions"""
        button_clicked = self.color_mode_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:
            self.settings.change_mode()
            self.settings.bg_color = self.settings.MODE.bg_color()
            self.settings.bullet_color = self.settings.MODE.bullet_color()

            self.play_button.button_color = self.settings.MODE.button_color()
            self.play_button.prep_msg()

            self.color_mode_button.button_color = self.settings.MODE.button_color()
            self.color_mode_button.prep_msg()

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
                self._update_lasers()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.stats.score >= self.stats.high_score:
                    self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_mode_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            if self.stats.score >= self.stats.high_score:
                self.stats.save_high_score()
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
            if bullet.rect.bottom <= 0 or bullet.rect.top >= self.settings.screen_height:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _fire_bullet(self):
        """Function to fire a bullet"""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.ship.make_fire_sound()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _fire_aliens_lasers(self):
        """Function to fire aliens lasers"""
        if len(self.lasers) < self.settings.lasers_allowed and self.game_active:
            if randint(0, 100) > 98:
                new_bullet = Laser(self)
                self.lasers.add(new_bullet)

    def _check_bullet_alien_collisions(self):
        """Function to check if a bullet collides with the alien"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    alien.make_crash_sound()
                    break

                self.stats.score += self.settings.alien_points * len(aliens)

            self.sb.prep_score()
            self.sb.check_high_score()

        self._new_level()

    def _new_level(self):
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Function for alien-ship hit"""
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_ship_left()

            self.bullets.empty()
            self.aliens.empty()

            # reset fleet and ship
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)

        else:
            self.ship.make_explosion_sound()
            self.game_active = False
            self.stats.ships_left -= 1
            self.sb.prep_ship_left()

    def _check_aliens_bottom(self):
        """Function to check if aliens have reached the bottom"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _update_lasers(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0 or laser.rect.top >= self.settings.screen_height:
                self.lasers.remove(laser)

        self._check_laser_ship_collisions()

    def _check_laser_ship_collisions(self):
        """Function to check if lasers have reached the ship"""
        collisions = pygame.sprite.spritecollideany(self.ship, self.lasers)

        if collisions:
            self.ship.make_explosion_sound()
            self.bullets.empty()
            self.sb.lives.empty()
            self.lasers.empty()
            self.game_active = False


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
