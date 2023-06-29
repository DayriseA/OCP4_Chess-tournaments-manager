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
        self.number_of_rounds = int(number_of_rounds)
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
        # self.participants.sort(key=lambda x: participants_scores[x], reverse=True)
        print("Before sorting:", self.participants)
        self.participants.sort(
            key=lambda x: participants_scores.get(x, 0), reverse=True
        )
        print("After sorting:", self.participants)
        print("Participants scores:", participants_scores)

    def initialize_next_round(self) -> None:
        """Initialize next round"""
        if self.current_round == 0:
            self.current_round += 1
            self.shuffle_participants()
            round_name = f"Round {self.current_round}"
            round = Round(round_name)
            print(f"=> {round_name} created. Setting up matches...")
            round.setup_matches(self.participants)
            self.rounds.append(round)
        elif self.current_round < self.number_of_rounds:
            self.current_round += 1
            self.sort_participants_by_score()
            round_name = f"Round {self.current_round}"
            round = Round(round_name)
            print(f"{round_name} created. Setting up matches...\n")
            round.setup_matches(self.participants)
            self.rounds.append(round)
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
            f"\nself.participants =\n {self.participants}"
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

    # def load_from_json(self) -> None:
    #     """Load tournaments from json file, if available."""
    #     if os.path.exists("datas/tournaments.json"):
    #         with open("datas/tournaments.json", "r") as file:
    #             json_data = json.load(file)
    #             self.tournaments = [Tournament(**data) for data in json_data]
    #             print("Tournaments successfully imported from datas/tournaments.json")
    #     else:
    #         print("datas/tournaments.json not found.")

    def load_from_json(self) -> None:
        """Load tournaments from json file, if available."""
        if os.path.exists("datas/tournaments.json"):
            with open("datas/tournaments.json", "r") as file:
                json_data = json.load(file)
                self.tournaments = []
                for data in json_data:
                    # Convert participants to list of Player objects
                    participants = [Player(**p) for p in data["participants"]]
                    # Convert rounds to list of Round objects
                    rounds = []
                    for r in data["rounds"]:
                        # Convert matches to list of Match objects
                        matches = []
                        for m in r["matches"]:
                            # Convert side1 and side2 to contain Player objects
                            player1 = Player(**m["side1"][0])
                            player2 = Player(**m["side2"][0])
                            points1 = m["side1"][1]
                            points2 = m["side2"][1]
                            player1_color = m["player1_color"]
                            match = Match(player1, player2, player1_color)
                            side1 = [player1, points1]
                            side2 = [player2, points2]
                            match.side1 = side1
                            match.side2 = side2
                            matches.append(match)
                        round = Round(r["name"], matches)
                        rounds.append(round)
                    tournament = Tournament(**data)
                    tournament.participants = participants
                    tournament.rounds = rounds
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
