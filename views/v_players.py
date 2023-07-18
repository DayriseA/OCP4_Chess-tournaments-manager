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

    def add_another_player(self):
        """Ask if the user want to add another player or not"""
        return input("Do you want to add another player? (y/n) ")

    def invalid_choice(self):
        """Message displayed when the user input an invalid choice"""
        print("Invalid choice")

    def show_message(self, message):
        """Generic print of a string"""
        print(message)

    def load_players(self, my_bool, path):
        """Display message if success or no"""
        if my_bool:
            print(f"Players list successfully loaded from {path}")
        else:
            print(f"{path} not found")

    def display_players(self, players):
        """Display a list of players"""
        for player in players:
            print(f"\n{player}")
        print(f"\n=> {len(players)} players displayed\n")

    def get_player_index(self) -> int:
        """Gets the user input for choosing a player"""
        try:
            choice = int(input("\nSelect a player by its index number: "))
            return choice
        except ValueError:
            print("That's not a valid number, try again")
