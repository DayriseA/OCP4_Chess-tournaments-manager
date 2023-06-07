"""Here is my main controller."""
from views.manager import ManagerView
from models.player import Player


class Controller:
    """Main controller. [WIP] for now, used for simple tests."""

    def __init__(self):
        self.view = ManagerView()

    def run(self):
        """Run the program. Now just used for simple tests."""
        if self.view.menu_prompt() == "1":
            self.add_players()
        else:
            print("Not implemented yet")

    def add_players(self):
        """
        Ask for players infos and store them in a list.
        Later, we will store them in a .json file.
        """
        players = []
        again = "y"
        while again == "y":
            player_infos = self.view.prompt_for_player_infos()
            player = Player(*player_infos)
            players.append(player)
            again = input("Do you want to add another player? (y/n) ")
        print(players)
