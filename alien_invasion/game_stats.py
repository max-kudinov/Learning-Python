class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, game):
        """Initialize statistics"""
        self.settings = game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics to their defaults"""
        self.ships_left = self.settings.ship_limit
