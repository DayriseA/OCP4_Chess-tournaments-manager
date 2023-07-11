"""Controller for tournaments management."""

from models.m_match import Match
from models.m_tournament import Tournament, TournamentsList
from models.m_players import PlayersList
from models.m_round import Round
from views.v_tournaments import TournamentsManagerView


class TournamentsController:
    """Controller class for tournaments management."""

    def __init__(self):
        self.view = TournamentsManagerView()
        self.players_list = PlayersList()
        self.tournaments_list = TournamentsList()

    def create_tournament(self):
        """Create a tournament"""
        tournament_info = self.view.ask_tournament_info()
        tournament = Tournament(**tournament_info)
        self.tournaments_list.add_tournament(tournament)
        self.tournaments_list.save_to_json()

    def select_tournament(self) -> Tournament:
        """Select a tournament from the tournaments list by its index."""
        selected_index = self.view.select_tournament(
            self.tournaments_list.tournaments
        )
        selected_tournament = self.tournaments_list.tournaments[selected_index]
        return selected_tournament

    def select_match(self, round_: Round) -> Match:
        """Select a match from the current round by its index."""
        selected_index = self.view.select_match(round_.matches)
        selected_match = round_.matches[selected_index]
        return selected_match

    def get_participants_by_id(self, number_of_participants: int) -> list:
        """Gets a list of players by their chess national ID"""
        participants = []
        while len(participants) < number_of_participants:
            chess_national_id = self.view.ask_participant_id()
            player = self.players_list.get_player_by_id(chess_national_id)
            if player is None:
                print("Unknown chess national ID, please try again\n")
            elif player in participants:
                print("This player is already selected\n")
            else:
                participants.append(player)
                print(f"{player.firstname} {player.lastname} added to the list")
        return participants

    def add_participants(self, tournament: Tournament):
        """Add participants to a tournament"""
        selection_method = self.view.ask_participants_selection_method()
        if selection_method == "1":
            participants = self.players_list.get_players_from_list(8)
            tournament.add_participants(participants)
        elif selection_method == "2":
            participants = self.get_participants_by_id(8)
            tournament.add_participants(participants)
        elif selection_method == "3":
            pass

    def modify_tournament_attributes(self, tournament: Tournament):
        """Modify attributes of a tournament"""
        quit_ = False
        while not quit_:
            choice = self.view.modify_attributes_menu()
            if choice == "1":
                tournament.name = input("New name: ")
                print(f"Name changed to {tournament.name}")
            elif choice == "2":
                tournament.location = input("New location: ")
                print(f"Location changed to {tournament.location}")
            elif choice == "3":
                tournament.start_date = input("New start date (DD-MM-YYYY): ")
                print(f"Starting date changed to {tournament.start_date}")
            elif choice == "4":
                tournament.end_date = input("New end date (DD-MM-YYYY): ")
                print(f"End date changed to {tournament.end_date}")
            elif choice == "5":
                tournament.number_of_rounds = input("New number of rounds: ")
                print(f"Number of rounds changed to {tournament.number_of_rounds}")
            elif choice == "6":
                tournament.description = input("New description: ")
                print("Description updated")
            elif choice == "7":
                quit_ = True
            else:
                print("Invalid choice")

    def read_or_modify_tournament(self, tournament: Tournament):
        """Consult or modify information of a tournament"""
        quit_ = False
        while not quit_:
            choice = self.view.read_modify_menu()
            if choice == "1":
                self.add_participants(tournament)
                self.tournaments_list.save_to_json()
            elif choice == "2":
                self.modify_tournament_attributes(tournament)
                self.tournaments_list.save_to_json()
            elif choice == "3":
                tournament.display_details()
            elif choice == "4":
                tournament.participants_by_alphabetical_order()
            elif choice == "5":
                tournament.display_rounds_and_matches()
            elif choice == "6":
                quit_ = True
            else:
                print("Invalid choice")

    def activate_tournament(self, tournament: Tournament):
        """When a tournament is started or resumed"""
        quit_ = False
        while not quit_:
            choice = self.view.tournament_active_menu()
            if choice == "1":  # Register a match result
                if tournament.current_round != 0:
                    round_ = tournament.rounds[tournament.current_round - 1]
                    match = self.select_match(round_)
                    player1_name = (
                            match.side1[0].firstname + " " + match.side1[0].lastname
                    )
                    player2_name = (
                            match.side2[0].firstname + " " + match.side2[0].lastname
                    )
                    result = self.view.ask_match_result(player1_name, player2_name)
                    match.set_result(result)
                    if round_.is_round_over():
                        round_.end_round()
                        tournament.update_scores()
                    self.tournaments_list.save_to_json()
                else:
                    print("==> No round has been initialized yet")
            elif choice == "2":
                if tournament.current_round == 0:
                    tournament.initialize_first_round()
                    self.tournaments_list.save_to_json()
                else:
                    tournament.initialize_next_round()
                    self.tournaments_list.save_to_json()
            elif choice == "3":
                quit_ = True
            else:
                print("Invalid choice")

    def run(self):
        """Run the tournaments' manager."""
        self.players_list.load_players()
        self.tournaments_list.load_from_json()
        self.tournaments_list.backup_tournaments()
        quit_ = False
        while not quit_:
            choice = self.view.base_menu()
            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                selected_tournament = self.select_tournament()
                self.read_or_modify_tournament(selected_tournament)
            elif choice == "3":
                active_tournament = self.select_tournament()
                self.activate_tournament(active_tournament)
            elif choice == "4":
                quit_ = True
            else:
                print("Invalid choice")
