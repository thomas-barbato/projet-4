"""import"""
from .validation import display_error
from .screen_and_sys_func import clear_screen
from .play_match_view import Playmatch
from .display_tournament_reports import TournamentReports
from .menu import TournamentMenu
from models.tables import Tournament
from controllers.tournament_controller import TournamentController
from rich import print
from rich.console import Console
from rich.table import Table


class DisplayTournaments:
    def __init__(self):
        self.selected_tournament_id = None
        self.console = Console()

    def display_all_tournaments(self):
        clear_screen(0)
        tournament_list = TournamentController().get_all_tournaments()
        self.console.print(
            "[bold][italic yellow]VOS TOURNOIS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        tournament_table = Table()
        tournament_table.add_column("id", justify="center", style="green", no_wrap=True)
        tournament_table.add_column("name", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("lieu", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("date début", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("date fin", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("nombre de tours", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("liste des joueurs", justify="center", style="white", no_wrap=False)
        tournament_table.add_column("control du temps", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("description", justify="center", style="white", no_wrap=True)
        for tournament in tournament_list:
            player_list = TournamentController(tournament).get_players_name_by_tournament_id(tournament["id"])
            tournament_table.add_row(
                str(tournament["id"]),
                tournament["tournament_name"],
                tournament["location"],
                tournament["tournament_date_begin"],
                tournament["tournament_date_end"],
                str(tournament["number_of_round"]),
                player_list,
                tournament["time_controller_choice"],
                tournament["description"],
            )
        print(tournament_table)
        self.select_tournament()

    def display_selected_tournaments(self, selected_tournament_instance):
        clear_screen(0)
        selected_tournament = selected_tournament_instance.set_data()
        self.console.print(
            "[bold][italic yellow]VOS TOURNOIS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        tournament_table = Table()
        tournament_table.add_column("id", justify="center", style="green", no_wrap=True)
        tournament_table.add_column("name", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("lieu", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("date début", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("date fin", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("nombre de tours", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("liste des joueurs", justify="center", style="white", no_wrap=False)
        tournament_table.add_column("control du temps", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("description", justify="center", style="white", no_wrap=True)
        player_list = TournamentController(selected_tournament).get_players_name_by_tournament_id(
            selected_tournament["id"]
        )
        tournament_table.add_row(
            str(selected_tournament["id"]),
            selected_tournament["tournament_name"],
            selected_tournament["location"],
            selected_tournament["tournament_date_begin"],
            selected_tournament["tournament_date_end"],
            str(selected_tournament["number_of_round"]),
            player_list,
            selected_tournament["time_controller_choice"],
            selected_tournament["description"],
        )
        print(tournament_table)

    def select_tournament(self):
        try:
            self.tournament_id = input("\n\nSelectionnez un identifiant (id): ")
            if not self.tournament_id:
                self.console.print(display_error("empty_field"))
                return self.select_tournament()
            else:
                if TournamentController().check_if_tournament_id_exists(int(self.tournament_id)) is True:
                    tournament_data = TournamentController().get_tournament_by_id(int(self.tournament_id))
                    tournament_model_instance = Tournament(tournament_data).unset_data(tournament_data)
                    if len(tournament_data["rounds"]) == int(tournament_data["number_of_round"]):
                        self.display_tournament_data_continue(tournament_model_instance)
                    else:
                        return Playmatch(tournament_model_instance).display_tournament_begin()
                else:
                    self.console.print(display_error("tournament_id_unknown"))
                    return self.select_tournament()
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.select_tournament()

    def display_tournament_data_continue(self, tournament_model_instance):
        print(tournament_model_instance.id)
        self.console.print(
            "[bold]\nCe tournoi est terminé.\n[/bold]"
            "[bold]\nVoulez-vous consulter les résultats ?\n[/bold]"
            "[italic]Appuyez sur [/italic]"
            "[bold green]'o'[/bold green] [italic] pour continuer ou [/italic][bold green]'n'[/bold green][italic]"
            " pour revenir au menu principal[/italic]\n\n"
        )
        response: str = input("Continuer (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_continue"))
            return self.display_tournament_data_continue()
        elif response.lower() == "n":
            return
        else:
            return TournamentReports().display_tournament_data(tournament_model_instance.id)
