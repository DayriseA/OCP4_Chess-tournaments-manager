"""
This module contains the Tournament class, a custom json encoder
and the TournamentsList class.
"""

import datetime
import json
import os
import random
import shutil

from models.m_match import Match
from models.m_players import Player
from models.m_round import Round


class Tournament:
    """The Tournament class"""

    def __init__(
        self,
        name: str,
        location: str,
        start_date=None,
        number_of_rounds: int = 4,
        description: str = "",
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = None
        self.number_of_rounds = int(number_of_rounds)
        self.current_round = 0
        self.rounds = []
        self.participants_scores = []
        self.description = description

    def add_participants(self, participants: list[Player]) -> None:
        """Add a list of participants to the tournament"""
        self.participants_scores = [(participant, 0) for participant in participants]

    def shuffle_participants(self) -> None:
        """Shuffle participants list"""
        random.shuffle(self.participants_scores)

    def update_scores(self) -> None:
        """Update participants scores according to every match result"""
        for i in range(len(self.participants_scores)):
            participant, score = self.participants_scores[i]
            score = 0
            for round_ in self.rounds:
                for match in round_.matches:
                    if (
                            match.side1[0].chess_national_id
                            == participant.chess_national_id
                    ):
                        score += match.side1[1]
                    elif (
                            match.side2[0].chess_national_id
                            == participant.chess_national_id
                    ):
                        score += match.side2[1]
            self.participants_scores[i] = (participant, score)

    def sort_participants_by_score(self) -> None:
        """
        Sort participants by score in descending order.
        Participants having the same score are shuffled between them.
        """
        self.participants_scores.sort(key=lambda x: x[1], reverse=True)
        i = 0
        while i < len(self.participants_scores):
            j = i + 1
            while (
                    j < len(self.participants_scores)
                    and self.participants_scores[j][1] == self.participants_scores[i][1]
            ):
                j += 1
            random.shuffle(self.participants_scores[i:j])
            i = j

    def participants_by_alphabetical_order(self) -> str:
        """Sort the participants by alphabetical order and return them as a str"""
        if len(self.participants_scores) > 0:
            participants = [player for player, score in self.participants_scores]
            participants.sort(key=lambda p: p.lastname)
            to_display = ""
            for participant in participants:
                to_display += f"\n{participant}\n"
            to_display += f"\n=> {len(participants)} participants displayed\n"
            return to_display
        else:
            info = "No participants registered yet"
            return info

    def already_played(self, player1_id, player2_id) -> bool:
        """Check if two players already played against each other"""
        for round_ in self.rounds:
            for match in round_.matches:
                if (
                        match.side1[0].chess_national_id == player1_id
                        and match.side2[0].chess_national_id == player2_id
                ) or (
                        match.side1[0].chess_national_id == player2_id
                        and match.side2[0].chess_national_id == player1_id
                ):
                    return True
        return False

    def setup_matches(self, next_round) -> str:
        """Set up matches of the next round received as argument."""
        # Avoid rematches.
        # If there is an odd number of participant, one will have to play 2 times.

        available_players = [player for player, score in self.participants_scores]
        if len(self.participants_scores) % 2 == 0:
            while available_players:
                player1 = available_players[0]
                for player2 in available_players[1:]:
                    if not self.already_played(
                            player1.chess_national_id, player2.chess_national_id
                    ):
                        match = Match(player1, player2)
                        next_round.matches.append(match)
                        available_players.remove(player1)
                        available_players.remove(player2)
                        break
                    else:
                        if len(available_players) == 2:
                            player1 = available_players[0]
                            player2 = available_players[1]
                            match = Match(player1, player2)
                            next_round.matches.append(match)
                            available_players.remove(player1)
                            available_players.remove(player2)
                            break
        else:
            while len(available_players) > 1:
                player1 = available_players[0]
                for player2 in available_players[1:]:
                    if not self.already_played(
                            player1.chess_national_id, player2.chess_national_id
                    ):
                        match = Match(player1, player2)
                        next_round.matches.append(match)
                        available_players.remove(player1)
                        available_players.remove(player2)
                        break
                    else:
                        if len(available_players) == 3:
                            player1 = available_players[0]
                            player2 = available_players[1]
                            match = Match(player1, player2)
                            next_round.matches.append(match)
                            available_players.remove(player1)
                            available_players.remove(player2)
                            break
            player_alone = available_players.pop()
            available_players = [player for player, score in self.participants_scores]
            # Avoid pairing with himself
            for player in available_players:
                if player_alone.chess_national_id == player.chess_national_id:
                    available_players.remove(player)
                    break
            for opponent in reversed(available_players):
                if not self.already_played(
                        player_alone.chess_national_id, opponent.chess_national_id
                ):
                    match = Match(player_alone, opponent)
                    next_round.matches.append(match)
                    break
        to_display = next_round.display_matches()
        return to_display

    def initialize_first_round(self) -> str:
        """Initialize first round"""
        if not self.participants_scores:
            msg = "==> No participants registered yet"
            return msg
        else:
            self.current_round += 1
            self.shuffle_participants()
            round_name = f"Round {self.current_round}"
            first_round = Round(round_name)
            msg = f"=> {round_name} created. Setting up matches...\n\n"
            msg += first_round.set_1st_round_matches(self.participants_scores)
            self.rounds.append(first_round)
            return msg

    def initialize_next_round(self) -> str:
        """Initialize next round"""
        self.update_scores()
        self.sort_participants_by_score()
        if self.current_round < self.number_of_rounds:
            self.current_round += 1
            round_name = f"Round {self.current_round}"
            next_round = Round(round_name)
            msg = f"{round_name} created. Setting up matches...\n"
            msg += self.setup_matches(next_round)
            self.rounds.append(next_round)
            return msg
        else:
            msg = "The tournament is finished"
            return msg

    def display_details(self) -> str:
        """Returns tournament detailed information as a str"""
        details = (
            f"\nTournament name: {self.name}\n"
            f"Location: {self.location}\n"
            f"Start date: {self.start_date}\n"
        )
        if self.end_date:
            details += f"End date: {self.end_date}\n"
        if self.current_round > 0:
            details += (
                f"Current round: {self.current_round} / "
                f"{self.number_of_rounds} planned\n"
            )
        else:
            details += (
                f"Number of rounds planned: {self.number_of_rounds} | "
                f"None initialized yet\n"
            )
        details += f"DESCRIPTION:\n{self.description}\n"
        return details

    def display_rounds_and_matches(self) -> str:
        """Return all rounds and matches as a str"""
        if len(self.rounds) > 0:
            msg = ""
            for round_ in self.rounds:
                msg += "\n"
                msg += round_.display_matches()
            return msg
        else:
            msg = "No rounds initialized yet"
            return msg

    def __str__(self) -> str:
        return f"{self.name}, starting on {self.start_date}, " f"in {self.location}"


class CustomEncoder(json.JSONEncoder):
    """Custom encoder to handle our complex objects and datetime objects"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return super().default(obj)


class TournamentsList:
    """A list of tournaments"""

    def __init__(self, tournaments: list[Tournament] = None):
        self.tournaments = tournaments or []

    def load_from_json(self, path: str) -> str:
        """Custom method for loading tournaments from json file (if available)."""
        if os.path.exists(path):
            with open(path, "r") as file:
                tournaments_data = json.load(file)
                for tournament_data in tournaments_data:
                    tournament = Tournament(
                        tournament_data["name"],
                        tournament_data["location"],
                        tournament_data["start_date"],
                        tournament_data["number_of_rounds"],
                        tournament_data["description"],
                    )
                    tournament.current_round = tournament_data["current_round"]
                    tournament.end_date = tournament_data["end_date"] or None
                    for participant_score_data in tournament_data[
                        "participants_scores"
                    ]:
                        participant_score = (
                            Player(
                                participant_score_data[0]["firstname"],
                                participant_score_data[0]["lastname"],
                                participant_score_data[0]["birthdate"],
                                participant_score_data[0]["chess_national_id"],
                            ),
                            participant_score_data[1],
                        )
                        tournament.participants_scores.append(participant_score)
                    for round_data in tournament_data["rounds"]:
                        round_ = Round(round_data["name"])
                        round_.start_date = datetime.datetime.fromisoformat(
                            round_data["start_date"]
                        )
                        if round_data["end_date"]:
                            round_.end_date = (
                                    datetime.datetime.fromisoformat(
                                        round_data["end_date"]
                                    )
                                    or None
                            )
                        for match_data in round_data["matches"]:
                            player1 = Player(
                                match_data["side1"][0]["firstname"],
                                match_data["side1"][0]["lastname"],
                                match_data["side1"][0]["birthdate"],
                                match_data["side1"][0]["chess_national_id"],
                            )
                            player2 = Player(
                                match_data["side2"][0]["firstname"],
                                match_data["side2"][0]["lastname"],
                                match_data["side2"][0]["birthdate"],
                                match_data["side2"][0]["chess_national_id"],
                            )
                            match = Match(player1, player2, match_data["player1_color"])
                            match.side1[1] = match_data["side1"][1]
                            match.side2[1] = match_data["side2"][1]
                            round_.matches.append(match)
                        tournament.rounds.append(round_)
                    self.tournaments.append(tournament)
            info = "Tournaments successfully imported from datas/tournaments.json"
            return info
        else:
            info = "datas/tournaments.json not found."
            return info

    @staticmethod
    def backup_tournaments(path: str) -> None:
        """Backup tournaments json file in a .bak file"""
        if os.path.exists(path):
            shutil.copy(path, path + ".bak")

    def add_tournament(self, tournament: Tournament) -> str:
        """Add a new tournament to our tournaments list"""
        if tournament not in self.tournaments:
            self.tournaments.append(tournament)
            info = f"{tournament.name} successfully added to the tournaments list\n"
            return info
        else:
            info = "This tournament is already registered\n"
            return info

    def save_to_json(self, path) -> str:
        """Save our tournaments list to a json file, at given path"""
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            json.dump(self.tournaments, file, cls=CustomEncoder, indent=4)
        info = "\n(Tournaments successfully saved to datas/tournaments.json)"
        return info

    def __str__(self):
        if len(self.tournaments) > 0:
            for tournament in self.tournaments:
                print(tournament)
            return f"\n=> {len(self.tournaments)} tournaments displayed\n"
        else:
            return "No tournaments found\n"
