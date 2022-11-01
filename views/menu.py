"""import"""

import os
import sys

PROJECT_CWD = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1])
sys.path.append(PROJECT_CWD)
sys.path.append(os.path.join(PROJECT_CWD, "controllers"))
sys.path.append(os.path.join(PROJECT_CWD, "views"))

from controllers.engine import Controller
from controllers.screen_and_sys_func import clear_screen, exit_to_console
from controllers.validation import display_error
from .tournament_create_choices_view import (
    display_description,
    display_location_tournament,
    display_number_of_round,
    display_number_of_turn,
    display_player_choice,
    display_player_list,
    display_save_tournament_choice,
    display_time_controller_choice,
    display_tournament_continue,
    display_tournament_date,
    display_tournament_name,
    display_confirm_tournament_choice,
)
from .menu_choices_view import display_menu_choices
import os
import sys
from rich import pretty, print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Menu:
    """_Menu_
    display frontend
    """

    def __init__(
        self,
    ):
        pretty.install()
        self.console = Console(width=100)
        self.display_main_menu()
        # controller_data = Controller

    def display_main_menu(self):
        """display_main_menu
        display main menu title and main menu
        loop as long as the entries are erroneous
        and redirect to selected choice view
        Returns:
            method
        """
        clear_screen(0)
        self.console.print(
            "[bold][italic yellow]GESTION TOURNOIS D'ECHECS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        menu_choices = display_menu_choices()
        if menu_choices == 1:
            self.display_create_tournament_menu()
        elif menu_choices == 2:
            pass
        elif menu_choices == 3:
            self.display_tournament_view()
        elif menu_choices == 4:
            pass
        elif menu_choices == 5:
            self.console.print("[italic red]Le programme va maintenant se terminer, à bientot.[/italic red]")
            clear_screen(1)
            exit_to_console(0)
        # deleted because it allways select 1st choice.
        """
        return {
            1: self.display_create_tournament_menu(),
            2: "okay lol",
            3: self.display_tournament_view(),
            5: exit_to_console(1, "[italic red]Le programme va maintenant se terminer, à bientot.[/italic red]"),
        }[menu_choices]"""

    def display_create_tournament_menu(self):
        controller_data = Controller
        """display_create_tournament_menu
        display tournament creation menu and title
        loop as long as the entries are erroneous
        Returns:
            dict : tournament data
        """
        clear_screen(0)
        self.console.print(
            "[bold][italic yellow]CREER UN NOUVEAU TOURNOI[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        self.console.print(
            "[bold]\nBienvenue dans le menu de création d'un nouveau tournoi.[/bold]"
            "[bold]\nVeuillez remplire correctement les informations suivantes:\n[/bold]"
            "[italic]Appuyez sur [/italic]"
            "[bold green]'o'[/bold green] [italic] pour continuer ou [/italic][bold green]'n'[/bold green][italic]"
            " pour revenir au menu principal[/italic]\n\n"
        )
        if display_tournament_continue() == "n":
            return self.display_main_menu()
        else:
            tournament_name = display_tournament_name()
            location = display_location_tournament()
            tournament_date_begin = display_tournament_date("begin")
            tournament_date_end = display_tournament_date("end")
            number_of_turn = display_number_of_turn()
            number_of_round = display_number_of_round()
            display_player_list()
            players_list = display_player_choice()
            time_controller_choice = display_time_controller_choice()
            description = display_description()

        self.console.print("[italic]\n\nVous allez maintenant être redirigé vers la page de sauvegarde[/italic]")
        self.tournament_data = {
            "tournament_name": tournament_name,
            "location": location,
            "tournament_date_begin": tournament_date_begin,
            "tournament_date_end": tournament_date_end,
            "number_of_turn": number_of_turn,
            "number_of_round": number_of_round,
            "players_list": players_list,
            "time_controller_choice": time_controller_choice,
            "description": description,
        }
        return self.display_save_tournament()

    def display_save_tournament(self):
        """display_save_tournament
        save tornament in database
        """
        controller_data = Controller()
        clear_screen(1)
        self.console.print(
            "[bold][italic yellow]CONFIRMER LA CREATION DE VOTRE TOURNOI[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        self.console.print(
            "[bold]\nDernière étape avant la création de votre nouveau tournois[/bold]"
            "[bold] Veuillez vérifier que les informations entrées sont correctes.\n[/bold]"
            "[italic]Appuyez sur [/italic]"
            "[bold green]'o'[/bold green][italic] pour sauvegarder ou [/italic][bold green]'n'[/bold green][italic]"
            " pour annuler et revenir au menu principal[/italic]\n\n"
        )

        print(
            Panel.fit(
                "[bold]Vos informations[/bold]\n\n"
                f"[bold green]Nom du tournoi:[/bold green] [bold]{self.tournament_data['tournament_name']}[/bold]\n"
                f"[bold green]Lieu du tournoi:[/bold green] [bold]{self.tournament_data['location']}[/bold]\n"
                f"[bold green]date début:[/bold green] [bold]{self.tournament_data['tournament_date_begin']}[/bold]\n"
                f"[bold green]date fin:[/bold green] [bold]{self.tournament_data['tournament_date_end']}[/bold]\n"
                f"[bold green]tour par ronde:[/bold green] [bold]{self.tournament_data['number_of_turn']}[/bold]\n"
                f"[bold green]ronde:[/bold green] [bold]{self.tournament_data['number_of_round']}[/bold]\n"
                f"[bold green]temps:[/bold green] [bold]{self.tournament_data['time_controller_choice']}[/bold]\n"
                f"[bold green]description:[/bold green] [bold]{self.tournament_data['description']}[/bold]\n",
                border_style="red",
            )
        )
        if len(controller_data.get_tournament_list()) >= 1:
            selected_players_table = Table(title="\n[bold]Liste des joueurs à inscrire à ce tournoi[/bold]\n")
            selected_players_table.add_column("id", justify="center", style="cyan", no_wrap=True)
            selected_players_table.add_column("Nom de famille", justify="center", style="white", no_wrap=True)
            selected_players_table.add_column("Prenom", justify="center", style="white", no_wrap=True)
            selected_players_table.add_column("rank", justify="center", style="green", no_wrap=True)

            for i in range(0, len(controller_data.get_players_list())):
                if controller_data.get_players_list()[i]["id"] in self.tournament_data["players_list"]:
                    selected_players_table.add_row(
                        str(controller_data.get_players_list()[i]["id"]),
                        str(controller_data.get_players_list()[i]["first_name"]),
                        str(controller_data.get_players_list()[i]["last_name"]),
                        str(controller_data.get_players_list()[i]["ranking"]),
                    )

            self.console.print(selected_players_table)
        if display_confirm_tournament_choice(self.tournament_data) == "n":
            return self.display_main_menu()
        else:
            return self.display_pairing_and_tournament()

    def display_pairing_and_tournament(self):
        controller_data = Controller()
        self.console.print(
            "[bold][italic yellow]VOTRE TOURNOIS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        self.console.print("\n[bold cyan]Paires de début de tournoi[/bold cyan]")
        controller_data.set_pairing(
            self.tournament_data["players_list"],
        )

    def display_tournament_view(self):
        controller_data = Controller()
        self.console.print(
            "[bold][italic yellow]CONSULTER LES TOURNOIS CRÉÉS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        if len(controller_data.get_tournament_list()) >= 1:
            table = Table(title="")
            table.add_column("id", justify="center", style="green", no_wrap=False)
            table.add_column("nom", justify="center", style="cyan", no_wrap=False)
            table.add_column("lieu", justify="center", style="cyan", no_wrap=False)
            table.add_column("date_debut", justify="center", style="cyan", no_wrap=False)
            table.add_column("date_fin", justify="center", style="cyan", no_wrap=False)
            table.add_column("nbr_tour", justify="center", style="cyan", no_wrap=False)
            table.add_column("nbr_manche", justify="center", style="cyan", no_wrap=False)
            table.add_column("time", justify="center", style="cyan", no_wrap=False)
            table.add_column("joueurs", justify="center", style="cyan", no_wrap=False)
            table.add_column("description", justify="center", style="cyan", no_wrap=False)

            for tournament in controller_data.get_tournament_list():
                table.add_row(
                    str(tournament["id"]),
                    str(tournament["name"]),
                    str(tournament["location"]),
                    str(tournament["tournament_date_begin"]),
                    str(tournament["tournament_date_end"]),
                    str(tournament["number_of_turn"]),
                    str(tournament["number_of_round"]),
                    str(tournament["time_controller_choice"]),
                    str(tournament["players_list"]),
                    str(tournament["description"]),
                )

            self.console.print(table)
            self.console.print(
                "[italic]\n\nAppuyez sur [/italic]"
                "[bold green]'o'[/bold green][italic] pour revenir au menu ou [/italic]"
                "[bold green]'q'[/bold green][italic]"
                " pour quitter[/italic]\n\n"
            )
            while True:
                response = input("Reponse (o / q): ")
                if response.lower() != "q" and response.lower() != "o":
                    self.console.print(display_error("wrong_input_choice_to_save"))
                elif response.lower() == "o":
                    self.console.print("[bold]vous allez être redirigé vers le menu principal.[/bold]")
                    clear_screen(1)
                    return self.display_main_menu()
                elif response.lower() == "q":
                    self.console.print("[bold]Le programme va maintenant se terminer, à très bientôt.\n[/bold]")
                    clear_screen(1)
                    return exit_to_console(0)
        else:
            self.console.print(display_error("no_tournament_created"))
            clear_screen(1)
            return self.display_create_tournament_menu()

    def display_create_player_menu(self):
        """display_create_player_menu
        display player creation menu and title
        loop as long as the entries are erroneous
        Returns:
            dict: player data
        """
        clear_screen(0)
