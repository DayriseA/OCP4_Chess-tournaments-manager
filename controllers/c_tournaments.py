"""Controller for tournaments management."""

from models.m_match import Match


class TournamentsController:
    """Controller class for tournaments management."""

    def __init__(self):
        pass

    def end_match(self, match: Match):
        """End a match and set the score"""
        player1_name = match.side1[0].firstname & match.side1[0].lastname
        player2_name = match.side2[0].firstname & match.side2[0].lastname
        choice = self.view.end_match_prompt(player1_name, player2_name)
        match.set_score(choice)
