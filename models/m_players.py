"""This module contains the Player class"""

from helpers import files_handler
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
        birthdate,
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

    def __repr__(self):
        return (
            f"\nself.firstname = {self.firstname}"
            f"\nself.lastname = {self.lastname}"
            f"\nself.birthdate = {self.birthdate}."
            f"\nself.chess_national_id = {self.chess_national_id}"
        )

    def __str__(self):
        return (
            f"{self.firstname} {self.lastname} | {self.birthdate} | "
            f"{self.chess_national_id}"
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

    def save_to_json(self) -> None:
        """Save our players list to a json file"""
        file_path = "datas/players.json"
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            json.dump([player.__dict__ for player in self.players], file, indent=4)
        print(f"{file_path} successfully saved")

    def __str__(self):
        if len(self.players) > 0:
            for player in self.players:
                print(player)
            return f"\n=> {len(self.players)} players displayed\n"
        else:
            return "No players found\n"
