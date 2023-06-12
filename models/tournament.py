"""This module contains the Tournament class"""

from models.round import Round
from models.player import Player
import datetime


class Tournament:
    """
    A Tournament and its attributes
    """

    def __init__(
        self,
        name: str,
        place: str,
        start_date=None,
        end_date=None,
        number_of_rounds: int = 4,
        rounds: list[Round] = None,
        players_and_score: list[tuple[Player, int]] = None,
        description: str = "",
    ):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.rounds = rounds or []
        self.players_and_score = players_and_score or []
        self.description = description
