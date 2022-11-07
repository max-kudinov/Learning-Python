class Settings:
    """Store settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""

        # Screen settings
        self.screen_width = 1024
        self.screen_height = 768

        # Graphic settings
        self.ship_image_scale = (57, 72)
        self.ships_left_image_scale = (38, 48)
        self.alien_image_scale = (60, 39)
        self.ship_image_path = "images/ship2.0.bmp"
        self.alien_image_path = "images/alien.bmp"
        self.bg_color = (35, 38, 52)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 3
        self.super_bullet = False  # goes through multiple targets
        self.bullet_color = (255, 205, 0)

        # Alien settings
        self.fleet_drop_speed = 10

        self.difficulty = ""
        self.score_increase = 10
        self.high_score_file = "high_score.json"

    def initialize_dynamic_settings(self):
        if self.difficulty == "easy":
            self.ship_speed = 0.2
            self.bullet_speed = 0.3
            self.alien_speed = 0.05
            self.speedup_scale = 1.1
            self.alien_points = 40

        elif self.difficulty == "medium":
            self.ship_speed = 0.3
            self.bullet_speed = 0.5
            self.alien_speed = 0.1
            self.speedup_scale = 1.4
            self.alien_points = 50

        elif self.difficulty == "hard":
            self.ship_speed = 0.5
            self.bullet_speed = 0.7
            self.alien_speed = 0.2
            self.speedup_scale = 1.7
            self.alien_points = 60

        self.fleet_direction = 1

    def increase_speed(self):
        """Increase the speed of the game"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points += self.score_increase
