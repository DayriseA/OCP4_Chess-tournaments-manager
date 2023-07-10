"""The main controller."""

from controllers.c_players import PlayersController
from controllers.c_tournaments import TournamentsController
from views.v_main import MainMenuView


class MainController:
    """Class for the main controller."""

    def __init__(self):
        self.menu_view = MainMenuView()

    def run(self):
        """Running the main controller"""
        quit_menu = False
        print("Welcome to Chess Tournament Manager!")
        while not quit_menu:
            choice = self.menu_view.main_menu()
            if choice == "1":
                players_manager = PlayersController()
                players_manager.run()
            elif choice == "2":
                tournaments_manager = TournamentsController()
                tournaments_manager.run()
            elif choice == "q":
                quit_menu = True
            else:
                print("Invalid choice")
