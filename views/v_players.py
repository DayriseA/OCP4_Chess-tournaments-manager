"""A view for the player's management."""


class PlayersManagerView:
    """A view class for the player's management."""

    def players_menu(self):
        """Displays the players manager's menu."""
        print("\nWhat do you want to do?")
        print("1. Add a player to our local base")
        print("2. Display all registered players by alphabetical order")
        print("3. Back to the main menu")
        choice = input("\nPress the number of your choice: ")
        return choice

    def ask_player_info(self):
        """Prompt for player information."""
        print("Please enter the following information for the player:")
        firstname = input("Firstname: ").capitalize()
        lastname = input("Lastname: ").upper()
        birthdate = input("Birthdate (DD-MM-YYYY): ")
        chess_national_id = input("Chess national ID: ").upper()
        return firstname, lastname, birthdate, chess_national_id
