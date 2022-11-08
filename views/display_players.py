"""import"""
from .validation import display_error, check_date_format
from .screen_and_sys_func import clear_screen
from views.menu import TournamentMenu
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import re


class DisplayPlayers:
    def __init__(self):
        self.console = Console()

    def display_all_players(self):
        print("ok")
