import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien"""

    def __init__(self, game):
        """Initialize an alien in a starting position"""

        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load the image for an alien
        self.image = pygame.image.load(self.settings.alien_image_path)
        self.image = pygame.transform.scale(self.image, self.settings.alien_image_scale)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
