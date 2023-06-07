"""This module contains the Player class"""


class Player:
    """
    A player has at least a firstname, a lastname and a birthdate
    """

    def __init__(
        self,
        firstname: str,
        lastname: str,
        birthdate,
        chess_national_id: str = "",
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.chess_national_id = chess_national_id

    def __repr__(self):
        return (
            f"{self.firstname} {self.lastname} born on {self.birthdate}."
            f"\nChess national ID: {self.chess_national_id}"
        )

    def __str__(self):
        return (
            f"{self.firstname} {self.lastname} born on {self.birthdate}."
            f"\nChess national ID: {self.chess_national_id}"
        )
