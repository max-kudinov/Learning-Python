import json


class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, game):
        """Initialize statistics"""
        self.settings = game.settings
        self.reset_stats()

        self.play_screen = True
        self.difficulty_select = False
        self.game_active = False

        self._read_high_score()

    def reset_stats(self):
        """Initialize statistics to their defaults"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _read_high_score(self):
        try:
            with open(self.settings.high_score_file) as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        with open(self.settings.high_score_file, "w") as f:
            json.dump(self.high_score, f)
