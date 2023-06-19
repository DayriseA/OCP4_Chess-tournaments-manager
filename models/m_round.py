"""This module contains the Round class"""
import datetime
import random
from models.m_match import Match
from models.m_players import Player


class Round:
    """ """

    def __init__(
        self,
        name: str,
        players_and_score: list[tuple[Player, int]] = None,
        matches: list[Match] = None,
    ):
        self.name = name
        self.players_and_score = players_and_score or []
        self.start_date = datetime.datetime.now()
        self.end_date = None
        self.matches = matches or []

    def first_shuffle_players(self):
        """Shuffle players list"""

        random.shuffle(self.players_and_score)

    def sort_by_score(self):
        """Sort players by score - descending order"""
        self.players_and_score.sort(key=lambda x: x[1], reverse=True)

    def create_matches(self):
        """Create matches by pairing players in order"""

        # Pair players by their order in the list
        for i in range(0, len(self.players_and_score) - 1, 2):
            player1, _ = self.players_and_score[i]
            player2, _ = self.players_and_score[i + 1]
            match = Match(player1, player2)
            self.matches.append(match)
