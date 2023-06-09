"""Controller for players' management."""
from models.m_players import Player, PlayersList
from views.v_players import PlayersManagerView


class PlayersController:
    """Controller class for players' management."""

    def __init__(self):
        self.view = PlayersManagerView()
        self.players_list = PlayersList()

    def add_players(self):
        """Ask for players information, create and add them to the players base."""
        again = "y"
        while again == "y":
            player_info = self.view.ask_player_info()
            player = Player(*player_info)
            self.players_list.add_player(player)
            self.players_list.save_to_json()
            again = input("Do you want to add another player? (y/n) ")

    def run(self):
        """Run the players' manager."""
        self.players_list.load_players()
        self.players_list.backup_players()
        quit_ = False
        while not quit_:
            choice = self.view.players_menu()
            if choice == "1":
                self.add_players()
            elif choice == "2":
                self.players_list.display_by_alphabetical_order()
            elif choice == "3":
                quit_ = True
            else:
                print("Invalid choice")
