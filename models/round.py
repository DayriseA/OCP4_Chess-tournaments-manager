"""This module contains the Round class"""
import datetime
import random
from models.match import Match
from models.player import Player


class Round:
    """ """

    def __init__(
        self,
        name: str,
        players_score_tuple: list[tuple[Player, int]] = None,
        matches: list[Match] = None,
    ):
        self.name = name
        self.players_score_tuple = players_score_tuple or []
        self.start_date = datetime.datetime.now()
        self.end_date = None
        self.matches = matches or []

    def first_shuffle_players(self):
        """Shuffle players list"""

        random.shuffle(self.players_score_tuple)

    def sort_by_score(self):
        """Sort players by score - descending order"""
        self.players_score_tuple.sort(key=lambda x: x[1], reverse=True)

    def create_matches(self):
        """Create matches by pairing players in order"""

        # Pair players by their order in the list
        for i in range(0, len(self.players_score_tuple) - 1, 2):
            player1, _ = self.players_score_tuple[i]
            player2, _ = self.players_score_tuple[i + 1]
            match = Match(player1, player2)
            self.matches.append(match)
