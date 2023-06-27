"""This module contains the Round class"""
import datetime
import random
from models.m_match import Match
from models.m_players import Player


class Round:
    """A round is mainly composed of a list of matches."""

    def __init__(
        self,
        name: str,
        matches: list[Match] = None,
    ):
        self.name = name
        self.start_date = datetime.datetime.now()
        self.end_date = None
        self.matches = matches or []
