"""Controller for players' management."""
from models.m_players import Player, PlayersList


class PlayersController:
    """Controller class for players' management."""

    JSON_PLAYERS_PATH = "datas/players.json"

    def __init__(self, view):
        self.view = view
        self.players_list = PlayersList()

    def add_players(self):
        """Ask for players information, create and add them to the players base."""
        again = "y"
        while again == "y":
            player_info = self.view.ask_player_info()
            player = Player(*player_info)
            msg = self.players_list.add_player(player)
            self.view.show_message(msg)
            msg = self.players_list.save_to_json("datas/players.json")
            self.view.show_message(msg)
            again = self.view.add_another_player()

    def get_player_from_list(self) -> Player:
        """Get a player by choosing him from our players list"""
        players_enumerated = self.players_list.enumerate_players()
        self.view.show_message(players_enumerated)
        choice = self.view.get_player_index()
        player = self.players_list.get_player_from_index(choice)
        return player

    def get_players_from_list(self, number_of_players: int) -> list[Player]:
        """Chose a determined number of players from our players list"""
        players = []
        while len(players) < number_of_players:
            player = self.get_player_from_list()
            if player is None:
                pass
            else:
                if player in players:
                    msg = "This player is already selected, try again\n"
                    self.view.show_message(msg)
                else:
                    players.append(player)
                    msg = f"{player.firstname} {player.lastname} added to the list"
                    self.view.show_message(msg)
        return players

    def run(self):
        """Run the players' manager."""
        success = self.players_list.load_players(self.JSON_PLAYERS_PATH)
        self.view.load_players(success, self.JSON_PLAYERS_PATH)
        self.players_list.backup_players(self.JSON_PLAYERS_PATH)
        quit_ = False
        while not quit_:
            choice = self.view.players_menu()
            if choice == "1":
                self.add_players()
            elif choice == "2":
                az_players = self.players_list.by_alphabetical_order()
                self.view.display_players(az_players)
            elif choice == "3":
                quit_ = True
            else:
                self.view.invalid_choice()
