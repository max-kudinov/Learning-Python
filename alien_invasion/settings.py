class Settings:
    """Store settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        self.screen_width = 1024
        self.screen_height = 768
        self.image_scale = (80, 105)
        self.image_path = "images/ship_cropped.bmp"
        self.bg_color = (35, 38, 52)
        self.ship_speed = 1.0
