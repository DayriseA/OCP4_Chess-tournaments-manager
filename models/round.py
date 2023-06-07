"""This module contains the Round class"""
import datetime


class Round:
    """
    A Round has a list of matches, a name, a start date and an end date.
    """

    def __init__(
        self,
        name: str,
        matches: list[Match] = None,
    ):
        self.name = name
        self.start_date = datetime.datetime.now()
        self.end_date = None
        self.matches = matches or []
