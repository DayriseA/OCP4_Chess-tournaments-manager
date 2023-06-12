"""The manager views."""


class ManagerView:
    """Manager view."""

    def menu_prompt(self):
        """Displays the menu prompt.[WIP]"""
        print("Welcome, what do you want to do?")
        print("\n1. Add a player to our local base")
        print("\n2. Display all registered players")
        print("\n\nType 'q' to quit the program")
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

    def end_match_prompt(self, player1_name, player2_name):
        """Prompt for the march result."""
        choice = input(
            "Select if:\n1. {} won\n2. {} won\n3. Draw\n".format(
                player1_name, player2_name
            )
        )
        return choice
