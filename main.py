"""
A simple program in CLI for managing chess tournaments offline.
Using MVC pattern. Datas are stored in .json files.
"""


from controllers.base import Controller


def main():
    """For now, just used for simple tests"""
    my_controller = Controller()
    my_controller.run()


if __name__ == "__main__":
    main()
