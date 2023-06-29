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
        print("2. Update a tournament")
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
        choice = input(
            "\nSelect how to chose the participants:\n"
            "1. From a list of players\n"
            "2. From their chess national ID\n"
        )
        return choice

    def participants_from_list_prompt(
        self, players_list: list, number_of_participants: int
    ) -> list:
        """Prompt to chose participants from a list of players."""
        print("\nPlease select the participants for the tournament:")
        for index, player in enumerate(players_list):
            print("{} - {}".format(index + 1, player))
        participants = []
        while len(participants) < number_of_participants:
            choice = int(input("Select a player: "))
            if choice not in range(1, len(players_list) + 1):
                print("Invalid choice")
            elif players_list[choice - 1] in participants:
                print("This player is already selected")
            else:
                participants.append(players_list[choice - 1])
                print(
                    "Player {} added to the tournament.".format(
                        players_list[choice - 1]
                    )
                )
        return participants

    def participants_from_id_prompt(
        self, players_list: list, number_of_participants: int
    ) -> list:
        """
        Prompt to chose participants from a list of players.
        Using the chess_national_id attribute.
        """
        participants = []
        known_ids = [player.chess_national_id for player in players_list]
        while len(participants) < number_of_participants:
            check_id = False
            while not check_id:
                choice = input(
                    "\nEnter the chess national ID of the participant to add: "
                ).upper()
                if choice not in known_ids:
                    print("Unknown ID, please try again.")
                elif choice in [player.chess_national_id for player in participants]:
                    print("This player is already selected")
                else:
                    check_id = True
            for player in players_list:
                if player.chess_national_id == choice:
                    participants.append(player)
                    print("Player {} added to the tournament.".format(player))
        return participants

    def get_tournament_index_prompt(self, tournaments_list: list) -> int:
        """From a list of tournaments, chose one by its index."""
        print("Please select the tournament:\n")
        for index, tournament in enumerate(tournaments_list):
            print(
                "{} - {} at {} starting {}".format(
                    index + 1,
                    tournament.name,
                    tournament.location,
                    tournament.start_date,
                )
            )
        choice = int(input("\nSelect a tournament (by typing index number): "))
        return choice - 1

    def tournament_update_prompt(self) -> str:
        """Chose what to update in the selected tournament."""
        print("\n Select what to do:\n")
        choice = input(
            "1. Register participants\n" "2. Modify attributes\n" "3. Back\n"
        )
        return choice

    def tournament_active_prompt(self) -> str:
        """Chose what to do with the selected tournament."""
        print("\n Select what to do:\n")
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
