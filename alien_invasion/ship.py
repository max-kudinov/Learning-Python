import pygame


class Ship:
    """A class to control the ship"""

    def __init__(self, game) -> None:
        """Initialize the ship in a starting position"""

        # Get initial game state
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        # Load the ship image
        self.image = pygame.image.load(self.settings.ship_image_path)
        self.image = pygame.transform.scale(self.image, self.settings.ship_image_scale)
        self.rect = self.image.get_rect()

        # Spawn the ship at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement
        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)

    def blitme(self):
        """Draws the ship at current position"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update ship coordinates"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.x > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
