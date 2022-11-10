from views.menu import TournamentMenu
from views.play_match_view import Playmatch
from views.screen_and_sys_func import clear_screen, exit_to_console
from views.validation import display_error
from views.create_player_view import CreatePlayer
from views.create_tournament_view import CreateTournament
from views.display_tournaments import DisplayTournaments
from views.display_players import DisplayPlayers
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class MainController:
    def __init__(self):
        self.display_menu = TournamentMenu()
        self.create_player_view = CreatePlayer()
        self.create_tournament_view = CreateTournament()
        self.display_tournaments = DisplayTournaments()
        self.display_players = DisplayPlayers()
        self.console = Console()

    def select_menu_choice(self):
        selected = self.display_menu.display_menu_choices()
        if selected == "1":
            return self.create_tournament_view.display_tournament_continue()
        elif selected == "2":
            return self.create_player_view.display_player_continue()
        elif selected == "3":
            return self.display_tournaments.display_all_tournaments()
        elif selected == "4":
            return self.display_players.display_all_players()
        elif selected == "5":
            clear_screen(0)
            self.console.print("[italic red]Le programme va maintenant se terminer, à bientot.[/italic red]")
            exit_to_console(0)
