# TODO: Docstring should contain a description of the file contains
# TODO: Sort imports using isort
from views.menu import TournamentMenu
from views.screen_and_sys_func import exit_to_console
from views.create_player_view import CreatePlayer
from views.create_tournament_view import CreateTournament
from views.display_tournaments import DisplayTournaments
from views.display_tournament_reports import TournamentReports
from views.display_players import DisplayPlayers

from rich.console import Console


class MainController:
    def __init__(self):
        self.display_menu = TournamentMenu()
        self.create_player_view = CreatePlayer()
        self.create_tournament_view = CreateTournament()
        self.display_tournaments = DisplayTournaments()
        self.display_players = DisplayPlayers()
        self.display_reports = TournamentReports()
        self.console = Console()

    def select_menu_choice(self):
        selected = self.display_menu.display_menu_choices()
        if selected == "1":
            self.create_tournament_view.display_tournament_continue()
        elif selected == "2":
            self.create_player_view.display_player_continue()
        elif selected == "3":
            self.display_tournaments.display_all_tournaments()
        elif selected == "4":
            self.display_players.display_all_players()
        elif selected == "5":
            self.display_reports.display_reports()
        if selected == "6":
            self.console.print("[italic red]Le programme va maintenant se terminer, à bientot.[/italic red]")
            exit_to_console(0)
        else:
            self.select_menu_choice()
