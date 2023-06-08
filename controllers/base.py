"""Here is my main controller."""
from views.manager import ManagerView
from models.player import Player, PlayerList
from helpers import files_handler


class Controller:
    """Main controller. [WIP] for now, used for simple tests."""

    def __init__(self):
        self.view = ManagerView()
        self.players_list = PlayerList()

    def load_players(self):
        """Load players from json file if available."""
        players_dict = files_handler.json_to_dict("datas/players.json")
        if players_dict:
            for player in players_dict:
                player = Player(**player)
                self.players_list.players.append(player)
            print("Players list successfully imported from datas/players.json\n")

    def run(self):
        """Run the program. Now just used for simple tests."""
        quit = False
        self.load_players()
        while not quit:
            if self.view.menu_prompt() == "1":
                self.add_players()
            elif self.view.menu_prompt() == "2":
                print(self.players_list)
            elif self.view.menu_prompt() == "q":
                quit = True
            else:
                print("Not implemented yet")

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
            files_handler.add_same_type_object_to_json(player, "datas/players.json")
            again = input("Do you want to add another player? (y/n) ")
        # files_handler.list_of_objects_to_json(players, "datas/players.json")
