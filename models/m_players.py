"""This module contains the Player class"""

from helpers import files_handler
from typing import List


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
        players_dict = files_handler.json_to_dict("datas/players.json")
        if players_dict:
            for player in players_dict:
                player = Player(**player)
                self.players.append(player)
            print("Players list successfully imported from datas/players.json")

    @staticmethod
    def backup_players() -> None:
        """Backup players.json file in a .bak file"""
        files_handler.copy_rename_file("datas/players.json", "datas/players.json.bak")

    def add_player(self, player: Player) -> None:
        """Add a new player to our players list"""
        if player.is_not_registered(self.players):
            self.players.append(player)
            print(f"{player} successfully added to the players list\n")
        else:
            print("This player is already registered\n")

    def save_to_json(self) -> None:
        """Save our players list to a json file"""
        files_handler.list_of_objects_to_json(self.players, "datas/players.json")

    def __str__(self):
        if len(self.players) > 0:
            for player in self.players:
                print(player)
            return f"\n=> {len(self.players)} players displayed\n"
        else:
            return "No players found\n"
