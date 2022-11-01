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

        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        """Moves alien sideways"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Returns true if alien has reached the edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
