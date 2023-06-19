"""A view for the tournaments management."""


class TournamentsManagerView:
    """A view class for the tournaments management."""

    def menu_prompt(self):
        """Displays the tournaments manager's menu.[WIP]"""
        pass

    def end_match_prompt(self, player1_name, player2_name):
        """Prompt for the march result."""
        choice = input(
            "Select if:\n1. {} won\n2. {} won\n3. Draw\n".format(
                player1_name, player2_name
            )
        )
        return choice
