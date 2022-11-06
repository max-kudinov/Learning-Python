class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, game):
        """Initialize statistics"""
        self.settings = game.settings
        self.reset_stats()

        self.play_screen = True
        self.difficulty_select = False
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics to their defaults"""
        self.ships_left = self.settings.ship_limit
