"""import"""
# from views.menu import TournamentMenu
from controllers.main_controller import MainController


def main():
    return MainController().select_menu_choice()


if __name__ == "__main__":
    main()
