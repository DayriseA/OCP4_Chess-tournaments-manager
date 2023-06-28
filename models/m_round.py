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

    def setup_matches(self, participants: list[Player]) -> None:
        """Set up the matches of the round by pairing participants."""
        if len(participants) % 2 != 0:
            for i in range(0, len(participants) - 1, 2):
                self.matches.append(Match(participants[i], participants[i + 1]))
            participants_exclude_last = participants[:-1]
            random_participant = random.choice(participants_exclude_last)
            self.matches.append(Match(random_participant, participants[-1]))

        elif len(participants) % 2 == 0:
            for i in range(0, len(participants), 2):
                self.matches.append(Match(participants[i], participants[i + 1]))

        print(f"{self.name} matches are set up:\n")
        for match in self.matches:
            player1_name = match.side1[0].firstname + " " + match.side1[0].lastname
            player2_name = match.side2[0].firstname + " " + match.side2[0].lastname
            color = match.player1_color
            print(f"{player1_name} (in {color} VS {player2_name}\n")
