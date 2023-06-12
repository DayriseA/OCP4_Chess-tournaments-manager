"""This module contains the Match class"""

from models.player import Player
import random


class Match:
    """A match is between two players"""

    def __init__(self, player1: Player, player2: Player):
        self.side1 = [player1, 0]
        self.side2 = [player2, 0]
        self.player1_color = random.choice(["white", "black"])

    def set_score(self, result):
        """Set the score of the match"""
        if result == "1":
            self.side1[1] = 1
            print(self.side1)
        elif result == "2":
            self.side2[1] = 1
            print(self.side2)
        elif result == "3":
            self.side1[1] = 0.5
            self.side2[1] = 0.5
            print(f"{self.side1}\n{self.side2}")
        else:
            print("Invalid input")
