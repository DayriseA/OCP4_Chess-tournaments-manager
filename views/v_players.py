"""A view for the players management."""


class PlayersManagerView:
    """A view class for the players management."""

    def menu_prompt(self):
        """Displays the players manager's menu."""
        print("What do you want to do?")
        print("\n1. Add a player to our local base")
        print("\n2. Display all registered players")
        print("\n3. Back to the main menu")
        choice = input("\nPress the number of your choice: ")
        return choice

    def prompt_for_player_infos(self):
        """Prompt for player infos."""
        print("Please enter the following informations for the player:")
        firstname = input("Firstname: ")
        lastname = input("Lastname: ")
        birthdate = input("Birthdate (DD-MM-YYYY): ")
        chess_national_id = input("Chess national ID: ")
        return (firstname, lastname, birthdate, chess_national_id)