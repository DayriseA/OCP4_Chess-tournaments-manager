"""Controller for tournaments management."""

from controllers.c_players import PlayersController
from models.m_match import Match
from models.m_round import Round
from models.m_tournament import Tournament, TournamentsList
from views.v_tournaments import TournamentsManagerView


class TournamentsController:
    """Controller class for tournaments management."""

    TOURNAMENTS_JSON_PATH = "datas/tournaments.json"

    def __init__(self, players_controller: PlayersController):
        self.view = TournamentsManagerView()
        self.players_controller = players_controller
        self.players_list = players_controller.players_list
        self.tournaments_list = TournamentsList()

    def create_tournament(self):
        """Create a tournament"""
        tournament_info = self.view.ask_tournament_info()
        tournament = Tournament(**tournament_info)
        info = self.tournaments_list.add_tournament(tournament)
        self.view.show_message(info)
        msg = self.tournaments_list.save_to_json(self.TOURNAMENTS_JSON_PATH)
        self.view.show_message(msg)

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
                msg = "Unknown chess national ID, please try again\n"
                self.view.show_message(msg)
            elif player in participants:
                msg = "This player is already selected\n"
                self.view.show_message(msg)
            else:
                participants.append(player)
                msg = f"{player.firstname} {player.lastname} added to the list\n"
                self.view.show_message(msg)
        return participants

    def add_participants(self, tournament: Tournament):
        """Add participants to a tournament"""
        selection_method = self.view.ask_participants_selection_method()
        if selection_method == "1":
            participants = self.players_controller.get_players_from_list(8)
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
                tournament.name = self.view.simple_prompt("New name: ")
                msg = f"Name changed to {tournament.name}"
                self.view.show_message(msg)
            elif choice == "2":
                tournament.location = self.view.simple_prompt("New location: ")
                msg = f"Location changed to {tournament.location}"
                self.view.show_message(msg)
            elif choice == "3":
                tournament.start_date = self.view.simple_prompt(
                    "New start date (DD-MM-YYYY): "
                )
                msg = f"Starting date changed to {tournament.start_date}"
                self.view.show_message(msg)
            elif choice == "4":
                tournament.end_date = self.view.simple_prompt(
                    "New end date (DD-MM-YYYY): "
                )
                msg = f"End date changed to {tournament.end_date}"
                self.view.show_message(msg)
            elif choice == "5":
                tournament.number_of_rounds = self.view.simple_prompt(
                    "New number of rounds: "
                )
                msg = f"Number of rounds changed to {tournament.number_of_rounds}"
                self.view.show_message(msg)
            elif choice == "6":
                tournament.description = self.view.simple_prompt("New description: ")
                self.view.show_message("Description successfully updated")
            elif choice == "7":
                quit_ = True
            else:
                self.view.show_message("Invalid choice")

    def read_or_modify_tournament(self, tournament: Tournament):
        """Consult or modify information of a tournament"""
        quit_ = False
        while not quit_:
            choice = self.view.read_modify_menu()
            if choice == "1":
                self.add_participants(tournament)
                msg = self.tournaments_list.save_to_json(self.TOURNAMENTS_JSON_PATH)
                self.view.show_message(msg)
            elif choice == "2":
                self.modify_tournament_attributes(tournament)
                msg = self.tournaments_list.save_to_json(self.TOURNAMENTS_JSON_PATH)
                self.view.show_message(msg)
            elif choice == "3":
                details = tournament.display_details()
                self.view.show_message(details)
            elif choice == "4":
                to_display = tournament.participants_by_alphabetical_order()
                self.view.show_message(to_display)
            elif choice == "5":
                to_display = tournament.display_rounds_and_matches()
                self.view.show_message(to_display)
            elif choice == "6":
                quit_ = True
            else:
                self.view.show_message("Invalid choice")

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
                    msg = match.set_result(result)
                    self.view.show_message(msg)
                    if round_.is_round_over():
                        msg = round_.end_round()
                        self.view.show_message(msg)
                        tournament.update_scores()
                    msg = self.tournaments_list.save_to_json(self.TOURNAMENTS_JSON_PATH)
                    self.view.show_message(msg)
                else:
                    msg = "==> No round has been initialized yet"
                    self.view.show_message(msg)
            elif choice == "2":
                if tournament.current_round == 0:
                    msg = tournament.initialize_first_round()
                    self.view.show_message(msg)
                    msg = self.tournaments_list.save_to_json(self.TOURNAMENTS_JSON_PATH)
                    self.view.show_message(msg)
                else:
                    msg = tournament.initialize_next_round()
                    self.view.show_message(msg)
                    msg = self.tournaments_list.save_to_json(self.TOURNAMENTS_JSON_PATH)
                    self.view.show_message(msg)
            elif choice == "3":
                quit_ = True
            else:
                self.view.show_message("Invalid choice")

    def run(self):
        """Run the tournaments' manager."""
        json_players_path = self.players_controller.JSON_PLAYERS_PATH
        success = self.players_list.load_players(json_players_path)
        self.players_controller.view.load_players(success, json_players_path)
        msg = self.tournaments_list.load_from_json(self.TOURNAMENTS_JSON_PATH)
        self.view.show_message(msg)
        self.tournaments_list.backup_tournaments(self.TOURNAMENTS_JSON_PATH)
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
                self.view.show_message("Invalid choice")
