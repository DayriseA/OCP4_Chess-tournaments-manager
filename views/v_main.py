"""A view for the main menu."""


class MainMenuView:
    """A view class displaying the main menu."""

    def main_menu(self):
        """Displays the main menu prompt."""
        print("\nWhat do you want to do?")
        print("1. Manage players")
        print("2. Manage tournaments")
        print("Type 'q' to quit the program")
        choice = input("\nPress the number of your choice: ")
        return choice
