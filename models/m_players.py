"""This module contains the Player and Players classes"""

import json
import os
import shutil
from typing import List


class Player:
    """A player has at least a firstname, a lastname and a birthdate."""

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

    def __str__(self):
        return (
            f"{self.firstname} {self.lastname}, né(e) le {self.birthdate}.\n"
            f"Chess national ID: {self.chess_national_id}"
        )


class PlayersList:
    """All our players list"""

    def __init__(self, players: List[Player] = None) -> None:
        self.players = players or []

    def load_players(self, path: str) -> bool:
        """Load players from json file at a given path, if available."""
        if os.path.exists(path):
            with open(path, "r") as file:
                json_data = json.load(file)
                self.players = [Player(**data) for data in json_data]
            return True
        else:
            return False

    @staticmethod
    def backup_players(path: str) -> None:
        """Backup players json file in a .bak file"""
        if os.path.exists(path):
            shutil.copy(path, path + ".bak")

    def is_not_registered(self, chess_national_id: str) -> bool:
        """Check if a player is already registered"""
        for player in self.players:
            if player.chess_national_id == chess_national_id:
                return False
        return True

    def add_player(self, player: Player) -> str:
        """Add a new player to our players list"""
        if self.is_not_registered(player.chess_national_id):
            self.players.append(player)
            msg = f"=> {player.firstname} {player.lastname} successfully added to " \
                  f"the players list\n"
            return msg
        else:
            msg = "This player is already registered\n"
            return msg

    def save_to_json(self, file_path: str) -> str:
        """Save our players list to a json file"""
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            json.dump([player.__dict__ for player in self.players], file, indent=4)
        return f"{file_path} successfully saved"

    def by_alphabetical_order(self) -> list:
        """Return a players list sorted by alphabetical order"""
        if len(self.players) > 0:
            players_sorted_az = sorted(self.players, key=lambda p: p.lastname)
            return players_sorted_az

    def get_player_by_id(self, chess_national_id: str) -> Player:
        """Gets a player by its chess national ID"""
        for player in self.players:
            if player.chess_national_id == chess_national_id:
                return player
        return None

    def enumerate_players(self) -> str:
        """Returns the players list and indexes (starting at 1) as a string"""
        players_list = ""
        if len(self.players) > 0:
            for index, player in enumerate(self.players, start=1):
                players_list += f"{index} - {player.firstname} {player.lastname}\n"
            return players_list
        else:
            return "No players found\n"

    def get_player_from_index(self, index: int) -> Player:
        """Gets a player from the players list by its index"""
        if len(self.players) > 0:
            if index in range(1, len(self.players) + 1):
                return self.players[index - 1]
            else:
                return None
        else:
            return None

    def __str__(self):
        if len(self.players) > 0:
            for player in self.players:
                print(player)
            return f"\n=> {len(self.players)} players displayed\n"
        else:
            return "No players found\n"
