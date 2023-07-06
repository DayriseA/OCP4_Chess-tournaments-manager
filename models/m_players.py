"""This module contains the Player class"""

from typing import List
import json, os, shutil


class Player:
    """
    A player has at least a firstname, a lastname and a birthdate
    """

    def __init__(
        self,
        firstname: str,
        lastname: str,
        birthdate: str,
        chess_national_id: str = "",
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.chess_national_id = chess_national_id

    def is_not_registered(self, players_list):
        """
        Check if a player is not already registered in our players list.
        Uses the chess national ID as primary key.
        """
        for player in players_list:
            if player.chess_national_id == self.chess_national_id:
                return False
        return True

    def __str__(self):
        return (
            f"{self.firstname} {self.lastname}, né(e) le {self.birthdate}.\n"
            f"Chess national ID: {self.chess_national_id}"
        )


class PlayersList:
    """All our players list"""

    def __init__(self, players: List[Player] = None) -> None:
        self.players = players or []

    def load_players(self) -> None:
        """Load players from json file, if available."""
        if os.path.exists("datas/players.json"):
            with open("datas/players.json", "r") as file:
                json_data = json.load(file)
                self.players = [Player(**data) for data in json_data]
            print("Players list successfully loaded from datas/players.json")
        else:
            print("datas/players.json not found")

    @staticmethod
    def backup_players() -> None:
        """Backup players.json file in a .bak file"""
        if os.path.exists("datas/players.json"):
            shutil.copy("datas/players.json", "datas/players.json.bak")

    def add_player(self, player: Player) -> None:
        """Add a new player to our players list"""
        if player.is_not_registered(self.players):
            self.players.append(player)
            print(f"{player} successfully added to the players list\n")
        else:
            print("This player is already registered\n")

    def is_registered(self, chess_national_id: str) -> bool:
        """Check if a player is already registered"""
        for player in self.players:
            if player.chess_national_id == chess_national_id:
                return True
        return False

    def save_to_json(self) -> None:
        """Save our players list to a json file"""
        file_path = "datas/players.json"
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            json.dump([player.__dict__ for player in self.players], file, indent=4)
        print(f"{file_path} successfully saved")

    def display_by_alphabetical_order(self) -> None:
        """Display players list by alphabetical order"""
        if len(self.players) > 0:
            for player in sorted(self.players, key=lambda p: p.lastname):
                print(f"\n{player}")
            print(f"\n=> {len(self.players)} players displayed\n")

    def get_player_by_id(self, chess_national_id: str) -> Player:
        """Gets a player by its chess national ID"""
        for player in self.players:
            if player.chess_national_id == chess_national_id:
                return player
        return None

    def get_player_from_list(self) -> Player:
        """Gets a player from the players list"""
        if len(self.players) > 0:
            for index, player in enumerate(self.players, start=1):
                print(f"{index} - {player.firstname} {player.lastname}")
            choice = int(input("\nSelect a player (by typing index number): "))
            if choice in range(1, len(self.players) + 1):
                return self.players[choice - 1]
            else:
                print("Invalid choice\n")
                return None
        else:
            print("No players found\n")
            return None

    def get_players_from_list(self, number_of_players: int) -> list:
        """Gets a list of players from the players list. Needs a number of players."""
        if len(self.players) > 0:
            players = []
            while len(players) < number_of_players:
                player = self.get_player_from_list()
                if player is None:
                    pass
                else:
                    if player in players:
                        print("This player is already selected\n")
                    else:
                        players.append(player)
                        print(f"{player.firstname} {player.lastname} added to the list")
            return players
        else:
            print("No players found\n")
            return []

    def __str__(self):
        if len(self.players) > 0:
            for player in self.players:
                print(player)
            return f"\n=> {len(self.players)} players displayed\n"
        else:
            return "No players found\n"
