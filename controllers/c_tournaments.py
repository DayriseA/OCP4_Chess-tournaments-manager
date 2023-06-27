"""Controller for tournaments management."""

from models.m_match import Match
from models.m_tournament import Tournament, TournamentsList
from models.m_players import PlayersList
from views.v_tournaments import TournamentsManagerView


class TournamentsController:
    """Controller class for tournaments management."""

    def __init__(self):
        self.view = TournamentsManagerView()
        self.players_list = PlayersList()
        self.tournaments_list = TournamentsList()

    # def end_match(self, match: Match):
    #     """End a match and set the score"""
    #     player1_name = match.side1[0].firstname & match.side1[0].lastname
    #     player2_name = match.side2[0].firstname & match.side2[0].lastname
    #     choice = self.view.end_match_prompt(player1_name, player2_name)
    #     match.set_score(choice)

    def create_tournament(self):
        """Create a tournament"""
        tournament_infos = self.view.tournament_infos_prompt()
        tournament = Tournament(**tournament_infos)
        self.tournaments_list.add_tournament(tournament)
        self.tournaments_list.save_to_json()

    def select_tournament(self) -> Tournament:
        """
        Select a tournament from the tournaments list by its index.
        Returns the tournament object.
        """
        selected_index = self.view.get_tournament_index_prompt(
            self.tournaments_list.tournaments
        )
        selected_tournament = self.tournaments_list.tournaments[selected_index]
        return selected_tournament

    def add_participants(self, tournament: Tournament):
        """Add participants to a tournament"""
        selection_method = self.view.participants_selection_method_prompt()
        if selection_method == "1":
            tournament.participants = self.view.participants_from_list_prompt(
                self.players_list.players, 8
            )
        elif selection_method == "2":
            tournament.participants = self.view.participants_from_id_prompt(
                self.players_list.players, 8
            )

    def update_tournament(self, tournament: Tournament):
        """Update a tournament"""
        quit = False
        while not quit:
            choice = self.view.tournament_update_prompt()
            if choice == "1":
                self.add_participants(tournament)
                self.tournaments_list.save_to_json()
            elif choice == "2":
                print(" => Not implemented yet")
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
                tournament_to_update = self.select_tournament()
                self.update_tournament(tournament_to_update)
            elif choice == "3":
                active_tournament = self.select_tournament()
                # later we will pass the tournament
                pass
            elif choice == "4":
                quit = True
            else:
                print("Invalid choice")
