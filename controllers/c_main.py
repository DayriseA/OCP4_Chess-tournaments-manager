"""The main controller."""

from controllers.c_players import PlayersController
from controllers.c_tournaments import TournamentsController
from views.v_main import MainMenuView
from views.v_players import PlayersManagerView


class MainController:
    """Class for the main controller."""

    def __init__(self):
        self.menu_view = MainMenuView()

    def run(self):
        """Running the main controller"""
        quit_menu = False
        self.menu_view.welcome()
        while not quit_menu:
            choice = self.menu_view.main_menu()
            if choice == "1":
                players_view = PlayersManagerView()
                players_controller = PlayersController(players_view)
                players_controller.run()
            elif choice == "2":
                players_view = PlayersManagerView()
                players_controller = PlayersController(players_view)
                tournaments_manager = TournamentsController(players_controller)
                tournaments_manager.run()
            elif choice == "q":
                quit_menu = True
            else:
                self.menu_view.invalid_choice()
