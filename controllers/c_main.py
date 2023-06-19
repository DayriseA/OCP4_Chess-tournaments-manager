"""The main controller."""

from controllers.c_players import PlayersController
from controllers.c_tournaments import TournamentsController
from views.v_main import MainMenuView


class MainController:
    """
    Class for the main controller.
    [WIP] For now used for simple tests.
    """

    def __init__(self):
        self.menu_view = MainMenuView()

    def run(self):
        """[WIP] Now just used for simple tests."""
        quit = False
        print("Welcome to Chess Tournament Manager!")
        while not quit:
            choice = self.menu_view.menu_prompt()
            if choice == "1":
                players_manager = PlayersController()
                players_manager.run()
            elif choice == "2":
                pass
            elif choice == "q":
                quit = True
            else:
                print("Invalid choice / Not implemented yet")
