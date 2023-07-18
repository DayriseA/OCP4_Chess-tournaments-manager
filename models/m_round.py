"""This module contains the Round class"""
import datetime
import random
from models.m_match import Match


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

    def set_1st_round_matches(self, participants_scores: list) -> str:
        """Set up the matches of the first round, using simple pairing."""
        participants = [participant for participant, score in participants_scores]
        if len(participants) % 2 != 0:
            for i in range(0, len(participants) - 1, 2):
                self.matches.append(Match(participants[i], participants[i + 1]))
            participants_exclude_last = participants[:-1]
            random_participant = random.choice(participants_exclude_last)
            self.matches.append(Match(random_participant, participants[-1]))

        elif len(participants) % 2 == 0:
            for i in range(0, len(participants), 2):
                self.matches.append(Match(participants[i], participants[i + 1]))

        msg = f"{self.name} matches set up as follow:\n"
        for match in self.matches:
            player1_name = match.side1[0].firstname + " " + match.side1[0].lastname
            player2_name = match.side2[0].firstname + " " + match.side2[0].lastname
            color = match.player1_color
            msg += f"{player1_name} (in {color} ) VS {player2_name}\n"
        return msg

    def is_round_over(self) -> bool:
        """Check if the round is over."""
        round_over = True
        for match in self.matches:
            if match.side1[1] == 0 and match.side2[1] == 0:
                round_over = False
                break
        return round_over

    def end_round(self) -> str:
        """Set the end date"""
        self.end_date = datetime.datetime.now()
        msg = f"{self.name} now ended.\n"
        return msg

    def display_matches(self) -> str:
        """Return the matches of the round as a str."""
        to_display = f"\n{self.name} matches:"
        for match in self.matches:
            to_display += f"\n{match}."
        return to_display

    def __str__(self) -> str:
        if self.end_date is None:
            return f"{self.name} started on {self.start_date}, still ongoing."
        else:
            return (
                f"{self.name} started on {self.start_date} "
                f"and ended on {self.end_date}."
            )
