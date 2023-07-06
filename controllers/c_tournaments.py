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
        tournament_infos = self.view.tournament_infos_prompt()
        tournament = Tournament(**tournament_infos)
        self.tournaments_list.add_tournament(tournament)
        self.tournaments_list.save_to_json()

    def select_tournament(self) -> Tournament:
        """Select a tournament from the tournaments list by its index."""
        selected_index = self.view.get_tournament_index_prompt(
            self.tournaments_list.tournaments
        )
        selected_tournament = self.tournaments_list.tournaments[selected_index]
        return selected_tournament

    def select_match(self, round: Round) -> Match:
        """Select a match from the current round by its index."""
        selected_index = self.view.select_match_prompt(round.matches)
        selected_match = round.matches[selected_index]
        return selected_match

    def get_participants_by_id(self, number_of_participants: int) -> list:
        """Gets a list of players by their chess national ID"""
        participants = []
        while len(participants) < number_of_participants:
            chess_national_id = self.view.participant_id_prompt()
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
        selection_method = self.view.participants_selection_method_prompt()
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
        quit = False
        while not quit:
            choice = self.view.modify_attributes_prompt()
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
                print(f"Description updated")
            elif choice == "7":
                quit = True
            else:
                print("Invalid choice")

    def read_or_modify_tournament(self, tournament: Tournament):
        """Consult or modify informations of a tournament"""
        quit = False
        while not quit:
            choice = self.view.read_modify_prompt()
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
                quit = True
            else:
                print("Invalid choice")

    def activate_tournament(self, tournament: Tournament):
        """When a tournament is started or resumed"""
        quit = False
        while not quit:
            choice = self.view.tournament_active_prompt()
            if choice == "1":
                if tournament.current_round != 0:
                    round = tournament.rounds[tournament.current_round - 1]
                    match = self.select_match(round)
                    player1_name = (
                        match.side1[0].firstname + " " + match.side1[0].lastname
                    )
                    player2_name = (
                        match.side2[0].firstname + " " + match.side2[0].lastname
                    )
                    result = self.view.end_match_prompt(player1_name, player2_name)
                    match.set_result(result)
                    if round.is_round_over() == True:
                        round.end_round()
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
                quit = True
            else:
                print("Invalid choice")

    def run(self):
        """Run the tournaments manager."""
        self.players_list.load_players()
        self.tournaments_list.load_from_json()
        self.tournaments_list.backup_tournaments()
        quit = False
        while not quit:
            choice = self.view.base_menu_prompt()
            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                selected_tournament = self.select_tournament()
                self.read_or_modify_tournament(selected_tournament)
            elif choice == "3":
                active_tournament = self.select_tournament()
                self.activate_tournament(active_tournament)
            elif choice == "4":
                quit = True
            else:
                print("Invalid choice")
