"""This module contains the Match class"""

from models.player import Player


class Match:
    """ """

    def __init__(self, player1: Player, player2: Player):
        self.side1 = [player1, 0]
        self.side2 = [player2, 0]
