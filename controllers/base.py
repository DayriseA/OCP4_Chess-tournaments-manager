"""Here is my main controller."""
from views.manager import ManagerView
from models.player import Player, PlayerList, Match
from helpers import files_handler


class Controller:
    """Main controller. [WIP] for now, used for simple tests."""

    def __init__(self):
        self.view = ManagerView()
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

    def run(self):
        """Run the program. Now just used for simple tests."""
        quit = False
        self.load_players()
        while not quit:
            choice = self.view.menu_prompt()
            if choice == "1":
                self.add_players()
            elif choice == "2":
                print(self.players_list)
            elif choice == "q":
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
            files_handler.list_of_objects_to_json(
                self.players_list.players, "datas/players.json"
            )
            again = input("Do you want to add another player? (y/n) ")

    def end_match(self, match: Match):
        """End a match and set the score"""
        player1_name = match.side1[0].firstname & match.side1[0].lastname
        player2_name = match.side2[0].firstname & match.side2[0].lastname
        choice = self.view.end_match_prompt(player1_name, player2_name)
        match.set_score(choice)
