"""Controller for players management."""
from models.m_players import Player, PlayerList
from views.v_players import PlayersManagerView
from helpers import files_handler


class PlayersController:
    """ "Controller class for players management."""

    def __init__(self):
        self.view = PlayersManagerView()
        self.players_list = PlayerList()

    def load_players(self):
        """Load players from json file if available."""
        files_handler.copy_rename_file("datas/players.json", "datas/players.json.bak")
        players_dict = files_handler.json_to_dict("datas/players.json")
        if players_dict:
            for player in players_dict:
                player = Player(**player)
                self.players_list.players.append(player)
            print("Players list successfully imported from datas/players.json\n")

    def add_players(self):
        """
        Ask for players infos and store them in a list.
        Later, we will store them in a .json file.
        """
        again = "y"
        while again == "y":
            player_infos = self.view.prompt_for_player_infos()
            player = Player(*player_infos)
            self.players_list.add_player(player)
            files_handler.list_of_objects_to_json(
                self.players_list.players, "datas/players.json"
            )
            again = input("Do you want to add another player? (y/n) ")

    def run(self):
        """Run the players manager."""
        self.load_players()
        quit = False
        while not quit:
            choice = self.view.menu_prompt()
            if choice == "1":
                self.add_players()
            elif choice == "2":
                print("\n")
                print(self.players_list)
            elif choice == "3":
                quit = True
            else:
                print("Invalid choice / Not implemented yet")
