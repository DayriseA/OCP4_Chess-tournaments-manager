"""
A simple program in CLI for managing chess tournaments offline.
Using MVC pattern. Datas are stored in .json files.
"""


from controllers.c_main import MainController


def main():
    """For now, just used for simple tests"""
    chess_app = MainController()
    chess_app.run()


if __name__ == "__main__":
    main()
