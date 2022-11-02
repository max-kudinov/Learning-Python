class Settings:
    """Store settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        self.screen_width = 1024
        self.screen_height = 768
        self.ship_image_scale = (57, 72)
        self.alien_image_scale = (60, 39)
        self.ship_image_path = "images/ship2.0.bmp"
        self.alien_image_path = "images/alien.bmp"
        self.bg_color = (35, 38, 52)
        self.ship_speed = 0.6
        self.bullet_speed = 0.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 205, 0)
        self.bullets_allowed = 3
        self.super_bullet = False
        self.alien_speed = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
