"""This module contains the Tournament class"""

from models.m_round import Round
from models.m_players import Player
from helpers import files_handler
import datetime
import random


class Tournament:
    """
    A Tournament and its attributes
    """

    def __init__(
        self,
        name: str,
        location: str,
        start_date=None,
        end_date=None,
        number_of_rounds: int = 4,
        current_round: int = 0,
        rounds: list[Round] = None,
        participants: list[Player] = None,
        description: str = "",
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.rounds = rounds or []
        self.participants = participants or []
        self.description = description

    def add_participants(self, participants: list[Player]) -> None:
        """Add a list of participants to the tournament"""
        self.participants = participants

    def shuffle_participants(self) -> None:
        """Shuffle participants list"""
        random.shuffle(self.participants)

    def sort_participants_by_score(self) -> None:
        """Sort participants by score in descending order."""
        participants_scores = {}
        for round in self.rounds:
            for match in round.matches:
                participant1 = match.side1[0]
                participant2 = match.side2[0]
                points1 = match.side1[1]
                points2 = match.side2[1]
                if participant1 not in participants_scores:
                    participants_scores[participant1] = 0
                if participant2 not in participants_scores:
                    participants_scores[participant2] = 0
                participants_scores[participant1] += points1
                participants_scores[participant2] += points2
        self.participants.sort(key=lambda x: participants_scores[x], reverse=True)

    def initialize_next_round(self) -> None:
        """"""
        pass

    def __str__(self):
        return (
            f"\nself.name = {self.name}"
            f"\nself.location = {self.location}"
            f"\nself.start_date = {self.start_date}"
            f"\nself.end_date = {self.end_date}"
            f"\nself.number_of_rounds = {self.number_of_rounds}"
            f"\nself.current_round = {self.current_round}"
            f"\nself.rounds =\n {self.rounds}"
            f"\nself.participants =\n {self.participants}"
            f"\nself.description =\n{self.description}"
        )


class TournamentsList:
    """A list of tournaments"""

    def __init__(self, tournaments: list[Tournament] = None):
        self.tournaments = tournaments or []

    def load_from_json(self) -> None:
        """Load tournaments from json file, if available."""
        tournaments_dict = files_handler.json_to_dict("datas/tournaments.json")
        if tournaments_dict:
            for tournament in tournaments_dict:
                tournament = Tournament(**tournament)
                self.tournaments.append(tournament)
            print("Tournaments successfully imported from tournaments.json")

    @staticmethod
    def backup_tournaments() -> None:
        """Backup tournaments.json file in a .bak file"""
        files_handler.copy_rename_file(
            "datas/tournaments.json", "datas/tournaments.json.bak"
        )

    def add_tournament(self, tournament: Tournament) -> None:
        """Add a new tournament to our tournaments list"""
        if tournament not in self.tournaments:
            self.tournaments.append(tournament)
            print(f"{tournament.name} successfully added to the tournaments list\n")
        else:
            print("This tournament is already registered\n")

    def save_to_json(self) -> None:
        """Save our tournaments list to a json file"""
        files_handler.list_of_objects_to_json(
            self.tournaments, "datas/tournaments.json"
        )

    def __str__(self):
        if len(self.tournaments) > 0:
            for tournament in self.tournaments:
                tournament.__str__()
            return f"\n=> {len(self.tournaments)} tournaments displayed\n"
        else:
            return "No tournaments found\n"
