from pathlib import Path

import pygame.font


class Button:

    def __init__(self, ai_game, msg, position='center', size=36):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # button dim and properties
        self.width, self.height = 400, 50
        self.message = msg
        self.button_color = ai_game.settings.MODE.button_color()
        self.text_color = "#000000"
        self.position = position
        self.font = pygame.font.Font(Path('../assets/fonts/CascadiaCode.ttf'), size)
        self.font.get_bold()

        # build the button
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg()

    def draw_button(self):
        """Draw the button on the screen"""
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def prep_msg(self):
        self.screen.fill(self.button_color, self.rect)

        self.msg_image = self.font.render(self.message, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()

        if self.position == 'center':
            self.msg_image_rect.center = self.rect.center
        if self.position == 'top_right':
            self.msg_image_rect.right = self.screen_rect.right - 20
            self.msg_image_rect.top = self.screen_rect.top + 20
        if self.position == 'top_left':
            self.msg_image_rect.left = self.screen_rect.left + 20
            self.msg_image_rect.top = self.screen_rect.top + 20
        if self.position == 'bottom_right':
            self.msg_image_rect.right = self.screen_rect.right - 20
            self.msg_image_rect.bottom = self.screen_rect.bottom - 20
        if self.position == 'bottom_left':
            self.msg_image_rect.left = self.screen_rect.left + 20
            self.msg_image_rect.bottom = self.screen_rect.bottom - 20

        self.rect.center = self.msg_image_rect.center
