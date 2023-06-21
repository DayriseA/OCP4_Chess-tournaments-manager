"""Controller for players management."""
from models.m_players import Player, PlayersList
from views.v_players import PlayersManagerView


class PlayersController:
    """ "Controller class for players management."""

    def __init__(self):
        self.view = PlayersManagerView()
        self.players_list = PlayersList()

    def add_players(self):
        """
        Ask for players infos, store them in a list and save the list in a json file.
        """
        again = "y"
        while again == "y":
            player_infos = self.view.prompt_for_player_infos()
            player = Player(*player_infos)
            self.players_list.add_player(player)
            self.players_list.save_to_json()
            again = input("Do you want to add another player? (y/n) ")

    def run(self):
        """Run the players manager."""
        self.players_list.load_players()
        quit = False
        while not quit:
            choice = self.view.menu_prompt()
            if choice == "1":
                self.players_list.backup_players()
                self.add_players()
            elif choice == "2":
                print("\n")
                print(self.players_list)
            elif choice == "3":
                quit = True
            else:
                print("Invalid choice")
