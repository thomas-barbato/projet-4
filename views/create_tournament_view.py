"""Display tournament creation view"""
import re

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from controllers.tournament_controller import TournamentController
from models.tables import Tournament
from views.create_player_view import CreatePlayer
from views.play_match_view import Playmatch

from .screen_and_sys_func import clear_screen
from .validation import check_date_format, display_error


class CreateTournament:
    def __init__(self):
        self.console = Console()
        self.tournament_name: str = ""
        self.location: str = ""
        self.tournament_date_begin: str = ""
        self.tournament_date_end: str = ""
        self.number_of_turn: int = 4
        self.number_of_round: int = 3
        self.player_list: list = []
        self.players_choice: list = []
        self.time_controller_choice: str = ""
        self.description: str = ""
        self.rounds: list = []
        self.id: int = 1
        self.pairing_round: tuple = ()
        self.create_player = CreatePlayer()
        self.tournament_controller = TournamentController()

    def tournament_data(self):
        return {
            "tournament_name": self.tournament_name,
            "location": self.location,
            "tournament_date_begin": self.tournament_date_begin,
            "tournament_date_end": self.tournament_date_end,
            "number_of_round": self.number_of_round,
            "players_choice": self.players_choice,
            "time_controller_choice": self.time_controller_choice,
            "description": self.description,
            "rounds": self.rounds,
            "id": self.id,
        }

    def display_create_menu(self):
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
        self.display_tournament_name()
        self.display_location_tournament()
        self.display_tournament_date("begin")
        self.display_tournament_date("end")
        self.display_number_of_round()
        self.display_player_list()
        self.display_player_choice()
        self.display_time_controller_choice()
        self.display_description()
        self.display_tournament_informations()
        self.display_confirm_tournament_save()

    def display_tournament_continue(self):
        clear_screen(0)
        self.console.print(
            "[bold]\nBienvenue dans le menu de création d'un nouveau tournoi.[/bold]"
            "[bold]\nVeuillez remplire correctement les informations suivantes:\n[/bold]"
            "[italic]Appuyez sur [/italic]"
            "[bold green]'o'[/bold green] [italic] pour continuer ou [/italic][bold green]'n'[/bold green][italic]"
            " pour revenir au menu principal[/italic]\n\n"
        )
        response: str = input("Continuer (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_continue"))
            clear_screen(1)
            self.display_tournament_continue()
        elif response.lower() == "o":
            self.display_create_menu()
        elif response.lower() == "n":
            from controllers.main_controller import MainController
            return MainController().select_menu_choice()

    def display_tournament_name(self):
        try:
            self.tournament_name = input("\n\nNom du tournoi: ")
            if not self.tournament_name:
                self.console.print(display_error("empty_field"))
                return self.display_tournament_name()
            else:
                return self.tournament_name
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.display_tournament_name()

    def display_location_tournament(self):
        try:
            self.location = input("\nLieu du tournoi: ")
            if not self.location:
                self.console.print(display_error("empty_field"))
                return self.display_location_tournament()
            else:
                return self.location
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.display_location_tournament()

    def display_tournament_date(self, temp):
        temp_input = {
            "begin": "\nDate et heure de début du tournoi (jj-mm-aaaa hh:mm): ",
            "end": "\nDate et heure de fin du tournoi (jj-mm-aaaa hh:mm): ",
        }
        try:
            self.tournament_date = input(temp_input[temp])
            if check_date_format(self.tournament_date) is False:
                self.console.print(display_error("date_format"))
                return self.display_tournament_date(temp)
            else:
                if temp == "begin":
                    self.tournament_date_begin = self.tournament_date
                else:
                    self.tournament_date_end = self.tournament_date
        except ValueError:
            self.console.print(display_error("date_format"))
            return self.display_tournament_date(temp)

    def display_number_of_round(self):
        self.number_of_round = input("\nNombre de ronde (3 par défaut si laissé vide): ")
        if self.number_of_round != "":
            if not (self.number_of_round.isdigit() and int(self.number_of_round) > 0):
                self.console.print(display_error("wrong_turn_type_entry"))
                return self.display_number_of_round()
            else:
                return int(self.number_of_round)
        else:
            # default value
            self.number_of_round = 3

    def display_player_list(self):
        # add here display limitation
        if len(self.tournament_controller.get_players_list()) >= 8:
            table = Table(title="\n\n[bold]Liste des joueurs à inscrire à ce tournoi[/bold]\n")
            table.add_column("Id", justify="center", style="cyan", no_wrap=True)
            table.add_column("Nom", justify="center", style="white", no_wrap=True)
            table.add_column("Prenom", justify="center", style="white", no_wrap=True)

            for player in self.tournament_controller.get_players_list():
                table.add_row(
                    str(player["id"]),
                    str(player["first_name"]),
                    str(player["last_name"]),
                )
            self.console.print(table)

        elif (
            len(self.tournament_controller.get_players_list()) > 0
            and len(self.tournament_controller.get_players_list()) <= 8
        ):
            self.console.print(display_error("too_few_player_created"))
            return self.create_player.display_player_continue()
        else:
            self.console.print(display_error("no_player_created"))
            return self.create_player.display_player_continue()

    def display_player_choice(self):
        self.console.print(
            "\n\n[bold]Veuillez selectionner [blue]8[/blue] joueurs parmis la liste présente[/bold]",
            "[bold]en entrant leurs numéro [blue]ID[/blue] séparés par un espace[/bold]",
        )
        set_players_choice = input("Entrez votre selection: ")
        # delete every character is not a number
        research = re.sub(r"[^0-9]", ",", set_players_choice)
        # store it in list
        self.players_choice = [int(nb) for nb in research.split(",") if nb != ""]
        # use len(set()) to delete doublon and check if len is okay.
        if len(set(self.players_choice)) < 8 or len(set(self.players_choice)) > 8:
            self.console.print(display_error("wrong_player_number_selected"))
            return self.display_player_choice()
        else:
            return self.players_choice

    def display_time_controller_choice(self):
        try:
            self.time_controller_choice = input("Tournée (blitz / bullet / coup rapide): ")
            if self.time_controller_choice == "" or not self.time_controller_choice.lower() in [
                "blitz",
                "bullet",
                "coup rapide",
            ]:
                self.console.print(display_error("time_controller_field"))
                return self.display_time_controller_choice()
            else:
                return self.time_controller_choice
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.display_time_controller_choice()

    def display_description(self):
        try:
            self.description = input("\nDescription du tournois (facultatif): ")
            return self.description
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.display_description()

    def display_tournament_informations(self):

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
            "[italic]pour annuler et revenir au menu principal[/italic]\n\n"
        )
        self.console.print(
            Panel.fit(
                f"[bold]Vos informations[/bold]\n\n"
                f"[bold green]Nom du tournoi:[/bold green] [bold]{self.tournament_data()['tournament_name']}[/bold]\n"
                f"[bold green]Lieu du tournoi:[/bold green] [bold]{self.tournament_data()['location']}[/bold]\n"
                f"[bold green]date début:[/bold green]"
                f"[bold]{self.tournament_data()['tournament_date_begin']}[/bold]\n"
                f"[bold green]date fin:[/bold green] [bold]{self.tournament_data()['tournament_date_end']}[/bold]\n"
                f"[bold green]ronde:[/bold green] [bold]{self.tournament_data()['number_of_round']}[/bold]\n"
                f"[bold green]temps:[/bold green] [bold]{self.tournament_data()['time_controller_choice']}[/bold]\n"
                f"[bold green]description:[/bold green] [bold]{self.tournament_data()['description']}[/bold]\n",
                border_style="red",
            )
        )
        if len(self.players_choice) == 8:
            selected_players_table = Table(title="\n[bold]Liste des joueurs à inscrire à ce tournoi[/bold]\n")
            selected_players_table.add_column("id", justify="center", style="cyan", no_wrap=True)
            selected_players_table.add_column("Nom de famille", justify="center", style="white", no_wrap=True)
            selected_players_table.add_column("Prenom", justify="center", style="white", no_wrap=True)
            for player in self.tournament_controller.get_players_list():
                if player["id"] in self.players_choice:
                    selected_players_table.add_row(
                        str(player["id"]),
                        player["first_name"],
                        player["last_name"],
                    )

            self.console.print(selected_players_table)

    def display_confirm_tournament_save(self):
        response = input("Confirmez les informations à sauvegarder (o/n): ")
        if response.lower() != "n" and response.lower() != "o":
            self.console.print(display_error("wrong_input_choice_to_confirm"))
            return self.display_confirm_tournament_save()
        else:
            if response.lower() == "o":
                data = [
                    self.tournament_name,
                    self.location,
                    self.tournament_date_begin,
                    self.tournament_date_end,
                    self.number_of_round,
                    self.players_choice,
                    self.time_controller_choice,
                    self.description,
                    self.rounds,
                    self.id,
                ]
                tournament_controller_data = TournamentController(data)
                tournament_controller_data.save()
                self.console.print("[bold]Sauvegarde terminée...[/bold]")
                clear_screen(1)
                self.display_confirm_begin_tournament()
            elif response.lower() == "n":
                self.console.print(
                    "\n[bold]Création annulée,[/bold]" "[bold]vous allez être redirigé vers le menu principal.[/bold]"
                )
                clear_screen(1)
                from controllers.main_controller import MainController
                return MainController().select_menu_choice()
            return response.lower()

    def display_confirm_begin_tournament(self):
        response = input("Voulez-vous commencer le tournois ? (o/n): ")
        if response.lower() != "n" and response.lower() != "o":
            self.console.print(display_error("wrong_input_choice_to_confirm"))
            return self.display_confirm_tournament_save()
        else:
            if response.lower() == "o":
                clear_screen(1)
                tournament_data = self.tournament_controller.get_tournament_by_name(self.tournament_name)
                tournament_model_instance = Tournament(tournament_data).unset_data(tournament_data)
                return Playmatch(tournament_model_instance).display_tournament_begin()
            elif response.lower() == "n":
                self.console.print("\n[bold]vous allez être redirigé vers le menu principal.[/bold]")
                clear_screen(1)
                from controllers.main_controller import MainController
                return MainController().select_menu_choice()
            return response.lower()
