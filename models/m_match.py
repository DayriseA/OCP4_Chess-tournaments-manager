"""This module contains the Match class"""

from models.m_players import Player
import random


class Match:
    """A match oppose two players and have a result when finished"""

    def __init__(self, player1: Player, player2: Player, color: str = None):
        self.side1 = [player1, 0]
        self.side2 = [player2, 0]
        self.player1_color = color or random.choice(["white", "black"])

    def set_result(self, result):
        """Set the result of the match"""
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

    def __str__(self):
        """Return names of the players and if they won, lost or draw"""
        player1_name = self.side1[0].firstname + " " + self.side1[0].lastname
        player2_name = self.side2[0].firstname + " " + self.side2[0].lastname
        if self.side1[1] == 1:
            return f"{player1_name} won against {player2_name}"
        elif self.side2[1] == 1:
            return f"{player2_name} won against {player1_name}"
        elif self.side1[1] == 0.5 and self.side2[1] == 0.5:
            return f"{player1_name} in a tie with {player2_name}"
        else:
            return f"Match not played yet"
