import pygame


class Ship:
    """A class to represent a ship"""

    def __init__(self, ai_game):
        """Initialise the ship"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # load ship image
        self.image = pygame.image.load('../assets/ship.bmp')
        self.rect = self.image.get_rect()

        # start ship at the bottom
        self.rect.midbottom = self.screen_rect.midbottom

        # store position
        self.x = float(self.rect.x)

        # Movement flags - at start ship does not move
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the position of the ship"""
        if self.moving_right and self.rect.right  < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update position
        self.rect.x = self.x

    def blit(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship at the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


