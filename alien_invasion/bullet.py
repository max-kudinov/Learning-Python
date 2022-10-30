import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class for controlling bullets"""

    def __init__(self, game):
        """Creates bullets in current ship location"""

        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Moves bullet up"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draws bullet on the screen"""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)
