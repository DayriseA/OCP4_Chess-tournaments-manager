"""This module contains the Tournament class"""

from models.m_round import Round
from models.m_players import Player
from models.m_match import Match
import datetime, random, json, os, shutil


class Tournament:
    """
    A Tournament and its attributes
    """

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
            for round in self.rounds:
                for match in round.matches:
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
        """Sort participants by score in descending order."""
        self.participants_scores.sort(key=lambda x: x[1], reverse=True)

    def already_played(self, player1_id, player2_id) -> bool:
        """Check if two players already played against each other"""
        for round in self.rounds:
            for match in round.matches:
                if (
                    match.side1[0].chess_national_id == player1_id
                    and match.side2[0].chess_national_id == player2_id
                ) or (
                    match.side1[0].chess_national_id == player2_id
                    and match.side2[0].chess_national_id == player1_id
                ):
                    return True
        return False

    def setup_matches(self, next_round) -> None:
        """Set up matches of the next round received as argument. Avoid rematches."""
        availables_players = [player for player, score in self.participants_scores]
        if len(self.participants_scores) % 2 == 0:
            while availables_players:
                player1 = availables_players[0]
                availables_players.remove(player1)
                for player2 in availables_players:
                    if not self.already_played(
                        player1.chess_national_id, player2.chess_national_id
                    ):
                        match = Match(player1, player2)
                        next_round.matches.append(match)
                        availables_players.remove(player2)
                        break
        else:
            while len(availables_players) > 1:
                player1 = availables_players[0]
                availables_players.remove(player1)
                for player2 in availables_players:
                    if not self.already_played(
                        player1.chess_national_id, player2.chess_national_id
                    ):
                        match = Match(player1, player2)
                        next_round.matches.append(match)
                        availables_players.remove(player2)
                        break
            player_alone = availables_players.pop()
            availables_players = [player for player, score in self.participants_scores]
            for opponent in reversed(availables_players):
                if not self.already_played(
                    player_alone.chess_national_id, opponent.chess_national_id
                ):
                    match = Match(player_alone, opponent)
                    next_round.matches.append(match)
                    break
        print(f"{next_round.name} matches set up as follow:\n")
        for match in next_round.matches:
            player1_name = match.side1[0].firstname + " " + match.side1[0].lastname
            player2_name = match.side2[0].firstname + " " + match.side2[0].lastname
            color = match.player1_color
            print(f"{player1_name} (in {color} ) VS {player2_name}")

    def initialize_first_round(self) -> None:
        """Initialize first round"""
        if not self.participants_scores:
            print("==> No participants registered yet")
        else:
            self.current_round += 1
            self.shuffle_participants()
            round_name = f"Round {self.current_round}"
            first_round = Round(round_name)
            print(f"=> {round_name} created. Setting up matches...")
            first_round.set_1st_round_matches(self.participants_scores)
            self.rounds.append(first_round)

    def initialize_next_round(self) -> None:
        """Initialize next round"""
        if self.current_round < self.number_of_rounds:
            self.current_round += 1
            self.update_scores()
            self.sort_participants_by_score()
            round_name = f"Round {self.current_round}"
            next_round = Round(round_name)
            print(f"{round_name} created. Setting up matches...\n")
            self.setup_matches(next_round)
            self.rounds.append(next_round)
        else:
            print("The tournament is finished")

    def __str__(self):
        return (
            f"\nself.name = {self.name}"
            f"\nself.location = {self.location}"
            f"\nself.start_date = {self.start_date}"
            f"\nself.end_date = {self.end_date}"
            f"\nself.number_of_rounds = {self.number_of_rounds}"
            f"\nself.current_round = {self.current_round}"
            f"\nself.rounds =\n {self.rounds}"
            f"\nself.participants_scores =\n {self.participants_scores}"
            f"\nself.description =\n{self.description}"
        )


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

    def load_from_json(self) -> None:
        """Load tournaments from json file, if available."""
        if os.path.exists("datas/tournaments.json"):
            with open("datas/tournaments.json", "r") as file:
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
                        round = Round(round_data["name"])
                        round.start_date = datetime.datetime.fromisoformat(
                            round_data["start_date"]
                        )
                        if round_data["end_date"]:
                            round.end_date = (
                                datetime.datetime.fromisoformat(round_data["end_date"])
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
                            round.matches.append(match)
                        tournament.rounds.append(round)
                    self.tournaments.append(tournament)
            print("Tournaments successfully imported from datas/tournaments.json")
        else:
            print("datas/tournaments.json not found.")

    @staticmethod
    def backup_tournaments() -> None:
        """Backup tournaments.json file in a .bak file"""
        if os.path.exists("datas/tournaments.json"):
            shutil.copy("datas/tournaments.json", "datas/tournaments.json.bak")

    def add_tournament(self, tournament: Tournament) -> None:
        """Add a new tournament to our tournaments list"""
        if tournament not in self.tournaments:
            self.tournaments.append(tournament)
            print(f"{tournament.name} successfully added to the tournaments list\n")
        else:
            print("This tournament is already registered\n")

    def save_to_json(self) -> None:
        """Save our tournaments list to a json file"""
        file_path = "datas/tournaments.json"
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            # json.dump(self.tournaments, file, default=lambda o: o.__dict__, indent=4)
            json.dump(self.tournaments, file, cls=CustomEncoder, indent=4)
        print("\n(Tournaments successfully saved to datas/tournaments.json)")

    def __str__(self):
        if len(self.tournaments) > 0:
            for tournament in self.tournaments:
                tournament.__str__()
            return f"\n=> {len(self.tournaments)} tournaments displayed\n"
        else:
            return "No tournaments found\n"
