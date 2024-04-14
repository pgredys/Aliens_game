import os
from datetime import datetime


def load_high_score():
    """Load high score from file"""
    try:
        with open('../high_score.log', 'r') as file:
            high_scores = []
            for line in file:
                score = line.split('::')[-1].strip()

                if score.isdigit() and int(score) >= 0:
                    high_scores.append(int(score))

                else:
                    score = 0
                    high_scores.append(score)

            high_scores.sort()
            high_scores.reverse()

            return high_scores[0]

    except FileNotFoundError:
        return 0

    except PermissionError:
        return 0


class GameStats:
    """Track stats for Aliens Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.level = None
        self.score = None
        self.ships_left = None
        self.settings = ai_game.settings
        self.reset_stats()

        self.high_score = load_high_score()

    def reset_stats(self):
        """Reset stats"""
        self.ships_left = self.settings.ships_limit

        self.score = 0
        self.level = 0

    def save_high_score(self):
        """Save high score to file"""
        today = datetime.now()

        high_score_str = f'[HIGH SCORE]::{today.strftime('%Y-%m-%d %H:%M:%S')}::{os.getlogin()}::{self.high_score}'
        with open('../high_score.log', 'a') as file:
            file.writelines(high_score_str + '\n')
