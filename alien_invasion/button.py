import pygame.font


class Button:
    """Creates a button with a text"""

    def __init__(self, game, msg):
        """Initializes button attributes"""

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Button parameters
        self.widht, self.height = 200, 50
        self.button_color = (7, 123, 6)
        self.text_color = (198, 208, 245)
        self.font = pygame.font.SysFont(None, 48)

        # Create button rectangle and place it in the center
        self.rect = pygame.Rect(0, 0, self.widht, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Makes a rectangle out of text and places it in the center"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
