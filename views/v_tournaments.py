"""A view for the tournaments management."""

from models.m_tournament import Tournament, TournamentsList
from models.m_round import Round
from models.m_match import Match


class TournamentsManagerView:
    """A view class for the tournaments management."""

    def base_menu_prompt(self):
        """Displays the tournaments manager's menu.[WIP]"""
        print("\nWhat do you want to do?")
        print("1. Create a new tournament")
        print("2. Consult or modify a tournament")
        print("3. Start/Resume a tournament")
        print("4. Back")
        choice = input("\nPress the number of your choice: ")
        return choice

    def tournament_infos_prompt(self) -> dict:
        """Prompt for tournament infos."""
        print("Please enter the following informations for the tournament:\n")
        name = input("Name: ")
        location = input("Location: ")
        start_date = input("Date (DD-MM-YYYY): ")
        number_of_rounds = input("Number of rounds: ")
        description = input("Description: ")
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "number_of_rounds": number_of_rounds,
            "description": description,
        }

    def participants_selection_method_prompt(self) -> str:
        """Pick a selection method for chosing the participants."""
        print("\nSelect how to chose the participants:")
        print("1. From a list of players")
        print("2. By their chess national ID")
        print("3. Cancel")
        choice = input("\nPress the number of your choice: ")
        return choice

    def participant_id_prompt(self) -> str:
        """Prompt for a chess national ID."""
        choice = input("\nEnter the chess national ID of the participant: ").upper()
        return choice

    def get_tournament_index_prompt(self, tournaments_list: list) -> int:
        """From a list of tournaments, chose one by its index."""
        print("\nPlease select the tournament:")
        for index, tournament in enumerate(tournaments_list):
            print(f"{index + 1} - {tournament}")
        choice = int(input("\nSelect a tournament (by typing index number): "))
        return choice - 1

    def modify_attributes_prompt(self) -> str:
        """Chose which information to modify."""
        print("\nSelect what to do:")
        print("1. Rename")
        print("2. Change location")
        print("3. Change starting date")
        print("4. Change ending date")
        print("5. Change number of rounds")
        print("6. Change description")
        print("7. Back")
        choice = input("\nPress the number of your choice: ")
        return choice

    def read_modify_prompt(self) -> str:
        """Chose what to update in the selected tournament."""
        print("\nSelect what to do:")
        print("1. Register participants")
        print("2. Modify attributes")
        print("3. Display tournament details")
        print("4. Display participants by alphabetical order")
        print("5. Display all rounds and matches results")
        print("6. Back")
        choice = input("\nPress the number of your choice: ")
        return choice

    def tournament_active_prompt(self) -> str:
        """Chose what to do with the selected tournament."""
        print("\nSelect what to do:")
        choice = input(
            "1. Register a match result\n" "2. Initialize next round\n" "3. Back\n"
        )
        return choice

    def select_match_prompt(self, matches: list[Match]) -> int:
        """Select a match from a list by its index."""
        print("Please select a match:\n")
        for index, match in enumerate(matches):
            print("{} - {}".format(index + 1, match))
        choice = int(input("\nSelect a match (by typing index number): "))
        return choice - 1

    def end_match_prompt(self, player1_name, player2_name) -> str:
        """Prompt for the match result."""
        choice = input(
            "Select if:\n1. {} won\n2. {} won\n3. Draw\n".format(
                player1_name, player2_name
            )
        )
        return choice
