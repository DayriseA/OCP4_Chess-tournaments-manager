"""A view for the main menu."""


class MainMenuView:
    """A view class displaying the main menu."""

    def menu_prompt(self):
        """Displays the main menu prompt."""
        print("What do you want to do?")
        print("\n1. Manage players")
        print("\n2. Manage tournaments")
        print("\n\nType 'q' to quit the program")
        choice = input("\nPress the number of your choice: ")
        return choice
