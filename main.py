"""
A simple program in CLI for managing chess tournaments offline.
Using MVC pattern. Datas are stored in .json files.
"""


from controllers.c_main import MainController


def main():
    """Run the app."""
    chess_app = MainController()
    chess_app.run()


if __name__ == "__main__":
    main()
