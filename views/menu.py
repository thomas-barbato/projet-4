"""import"""
import os
import sys
import re

PROJECT_CWD = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1])
sys.path.append(PROJECT_CWD)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, "controllers"))
from time import sleep
import datetime
from controllers.engine import Controller
from models.tables import Tournament, Player
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
        self.menu_choices: int = 0
        self.controller_data: Controller =  Controller()
        self.display_main_menu()

    def _clear_screen(self, sleep_val: int = 0):
        """_clear_screen_
        Args:
            sleep_val (int, optional): _sleep_val_. Defaults to 0.
        clear screen
        """
        sleep(sleep_val)
        return os.system("cls")

    def _exit(self, sleep_val: int = 0):
        """_exit_
        Args:
            sleep_val (int, optional): _description_. Defaults to 0.
        exit program
        """
        sleep(sleep_val)
        return os.system("exit")

    def get_main_menu_choices(self):
        """_get_main_menu_choices_
        Returns:
            _int_: _menu_choice_
        """
        return self.menu_choices

    def _return_msg_error(self, category: str):
        """_return_msg_error_
        Args:
            category (str): _description_
        show error msg.
        """
        return {
            "main_choice_value": "[italic red]Veuillez entrer une valeur numérique comprise entre 1 et 5...\n[/italic red]\n",
            "main_choice_type": "[italic red]Veuillez entrer une valeur numérique...\n[/italic red]\n",
            "wrong_input_choice_to_continue":"[italic red]Appuyez sur [/italic red][bold]'o'[/bold][italic red] pour continuer ou"\
                "[/italic red][bold green] 'n'[/bold green][italic red] pour revenir au menu principal[/italic red]\n",
            "empty_field": "[italic red]Veuillez renseigner ce champ[/italic red]",
            "date_format": "[italic red]Format de date incorrect, format attendu: jj-mm-aaaa hh:mm\nExemple: "\
                "[bold]10-09-2022 10:30[/bold][/italic red]\n",
            "wrong_turn_type_entry": "[italic red]Veuillez entrer une valeur correcte, format attendu: "\
                "[bold]un entier positif superieur à 0[/bold][/italic red]\n",
            "time_controller_field":  "[italic red]Veuillez entrer une valeur correcte, choix attendu:"\
                "[bold] blitz[/bold] ou [bold]bullet[/bold] ou [bold]coup_rapide[/bold][/italic red]\n",
            "no_player_created": "[italic red]\n\nVous n'avez pas encore inscrit de joueur.[/bold][/italic red]"\
                "\n\n[bold]Vous allez être redirigé vers la page d'inscription de nouveaux joueurs.[/bold]",
            "too_few_player_created": "[italic red]\n\nVeuillez d'abord inscrire au moins[bold] 8 joueurs[/bold][/italic red]"\
                "[italic red] afin de pouvoir les assigner à un tournois[/italic red]"\
                "\n\n[bold]Vous allez être redirigé vers la page d'inscription de nouveaux joueurs.[/bold]",
            "wrong_player_number_selected": "[italic red]Veuillez selectionner[bold] 8 joueurs[/bold][/italic red]",
            "no_tournament_created": "[italic red][bold]\n\nVous n'avez pas encore créé de tournoi.[/bold][/italic red]"\
                "\n\n[bold]Vous allez être redirigé vers la page de création de tournois.[/bold]"
                
        }[category]

    def _check_date_format(self, date: str):
        try:
            datetime.datetime.strptime(date, "%d-%m-%Y %H:%M")
            return True
        except ValueError:
            return False

    def display_main_menu(self):
        """display_main_menu
        display main menu title and main menu
        loop as long as the entries are erroneous
        and redirect to selected choice view
        Returns:
            method
        """
        while True:
            self.console.print(
                "[bold][italic yellow]GESTION TOURNOIS D'ECHECS[/italic yellow][/bold]\n",
                style=None,
                justify="center",
            )
            print(
                Panel.fit(
                    "[bold green]Menu:[/bold green]\n\n"
                    "[bold green]1)[/bold green] [bold]Créer un nouveau tournoi[/bold]\n"
                    "[bold green]2)[/bold green] [bold]Inscrire un nouveau joueur[/bold]\n"
                    "[bold green]3)[/bold green] [bold]Consulter les tournois créés[/bold]\n"
                    "[bold green]4)[/bold green] [bold]Consulter les joueurs inscrits[/bold]\n"
                    "[bold green]5)[/bold green] [bold]Quitter[/bold]",
                    border_style="red",
                )
            )
            try:
                self.menu_choices = int(input("Entrez votre choix: "))
                if not (self.menu_choices >= 1 and self.menu_choices <= 5):
                    self.console.print(self._return_msg_error("main_choice_value"))
                    self._clear_screen(1)
                else:
                    break
            except ValueError:
                self.console.print(self._return_msg_error("main_choice_type"))
                self._clear_screen(1)
        if self.menu_choices == 1:
            self.display_create_tournament_menu()
        elif self.menu_choices == 2:
            self.display_create_player_menu()
        elif self.menu_choices == 3:
            self.display_tournament_view()
        elif self.menu_choices == 5:
            self.console.print("[italic red]Le programme va maintenant se terminer, à très bientôt.\n[/italic red]")
            self._clear_screen(1)
            return self._exit(1)

    def display_create_tournament_menu(self):
        """display_create_tournament_menu
        display tournament creation menu and title
        loop as long as the entries are erroneous
        Returns:
            dict : tournament data
        """
        self._clear_screen(0)
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

        while True:
            response = input("Continuer (o/n): ")
            if response.lower() != "n" and response.lower() != "o":
                self.console.print(self._return_msg_error("wrong_input_choice_to_continue"))
            elif response.lower() == "o":
                break
            elif response.lower() == "n":
                self._clear_screen(0)
                return self.display_main_menu()

        while True:
            try:
                tournament_name = input("\n\nNom du tournoi: ")
                if not tournament_name:
                    self.console.print(self._return_msg_error("empty_field"))
                else:
                    break
            except ValueError:
                self.console.print(self._return_msg_error("empty_field"))

        while True:
            try:
                location = input("\nLieu du tournoi: ")
                if not location:
                    self.console.print(self._return_msg_error("empty_field"))
                else:
                    break
            except ValueError:
                self.console.print(self._return_msg_error("empty_field"))

        while True:
            try:
                tournament_date_begin = input("\nDate et heure de début du tournoi (jj-mm-aaaa hh:mm): ")
                if self._check_date_format(tournament_date_begin) is False:
                    self.console.print(self._return_msg_error("date_format"))
                else:
                    break
            except ValueError:
                self.console.print(self._return_msg_error("date_format"))

        while True:
            try:
                tournament_date_end = input("\nDate et heure de fin du tournoi (jj-mm-aaaa hh:mm): ")
                if self._check_date_format(tournament_date_end) is False:
                    self.console.print(self._return_msg_error("date_format"))
                else:
                    break
            except ValueError:
                self.console.print(self._return_msg_error("date_format"))

        while True:
            number_of_turn = input("\nTours par manche (4 par défaut si laissé vide): ")
            if number_of_turn != "":
                if not (number_of_turn.isdigit() and int(number_of_turn) > 0):
                    self.console.print(self._return_msg_error("wrong_turn_type_entry"))
                else:
                    number_of_turn = int(number_of_turn)
                    break
            else:
                number_of_turn = 4
                break

        while True:
            number_of_round = input("\nNombre de ronde (3 par défaut si laissé vide): ")
            if number_of_round != "":
                if not (number_of_round.isdigit() and int(number_of_round) > 0):
                    self.console.print(self._return_msg_error("wrong_turn_type_entry"))
                else:
                    number_of_round = int(number_of_round)
                    break
            else:
                number_of_round = 3
                break

        if len(self.controller_data.get_players_list()) >= 8:
            table = Table(title="\n\n[bold]Liste des joueurs à inscrire à ce tournoi[/bold]\n")
            table.add_column("id", justify="center", style="cyan", no_wrap=True)
            table.add_column("nom", justify="center", style="magenta", no_wrap=True)
            table.add_column("Prenom", justify="center", style="green", no_wrap=True)

            for player in self.controller_data.get_players_list():
                table.add_row(
                    str(player["id"]),
                    str(player["last_name"]),
                    str(player["first_name"]),
                )
            console = Console()
            console.print(table)
            while True:
                console.print(
                    "\n\n[bold]Veuillez selectionner [blue]8[/blue] joueurs parmis la liste présente[/bold]",
                    "[bold]en entrant leurs numéro [blue]ID[/blue] séparés par un espace[/bold]",
                )
                players_list = input("Entrez votre selection: ")
                # delete every character is not a number
                research = re.sub(r"[^0-9]", ",", players_list)
                # store it in list
                players_list = [int(nb) for nb in research.split(",") if nb != ""]
                if len(players_list) < 8 or len(players_list) > 8:
                    self.console.print(self._return_msg_error("wrong_player_number_selected"))
                else:
                    break

        elif len(self.controller_data.get_players_list()) <= 8 and len(self.controller_data.get_players_list()) > 0:
            self.console.print(self._return_msg_error("too_few_player_created"))
            # redirection here...
        else:
            self.console.print(self._return_msg_error("no_player_created"))
            # redirection here...

        while True:
            try:
                time_controller_choice = input("Tournée (blitz / bullet / coup_rapide): ")
                if time_controller_choice and self.controller_data.check_enum_status(time_controller_choice) is False or not time_controller_choice:
                    self.console.print(self._return_msg_error("time_controller_field"))
                else:
                    break
            except ValueError:
                self.console.print(self._return_msg_error("empty_field"))

        while True:
            try:
                description = input("\nDescription du tournois: ")
                if not description:
                    self.console.print(self._return_msg_error("empty_field"))
                else:
                    break
            except ValueError:
                self.console.print(self._return_msg_error("empty_field"))

        console.print("[italic]\n\nVous allez maintenant être redirigé vers la page de sauvegarde[/italic]")
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
        self._clear_screen(1)
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
                f"[bold green]Liste des joueurs:[/bold green] [bold]{self.tournament_data['players_list']}[/bold]\n"
                f"[bold green]temps:[/bold green] [bold]{self.tournament_data['time_controller_choice']}[/bold]\n"
                f"[bold green]description:[/bold green] [bold]{self.tournament_data['description']}[/bold]\n",
                border_style="red",
            )
        )
    
        while True:
            response = input("sauvegarder (o/n): ")
            if response.lower() != "n" and response.lower() != "o":
                self.console.print(self._return_msg_error("wrong_input_choice_to_save"))
            elif response.lower() == "o":
                tournament = Tournament(self.tournament_data)
                tournament.save()
                self.console.print(
                    "\n[bold]Le tournoi a été correctement sauvegardé,[/bold]"
                    "[bold]vous allez être redirigé vers le menu principal.[/bold]"
                )
                self._clear_screen(1)
                return self.display_main_menu()
            elif response.lower() == "n":
                self._clear_screen(0)
                return self.display_main_menu()
    
    def display_tournament_view(self):
        self.console.print(
            "[bold][italic yellow]CONSULTER LES TOURNOIS CRÉÉS[/italic yellow][/bold]\n",
            style=None,
            justify="right",
        )
        if len(self.controller_data.get_tournament_list()) >= 1:
            table = Table(title="\n\n[bold]Liste des joueurs à inscrire à ce tournoi[/bold]\n")
            table.add_column("id", justify="center", style="green", no_wrap=True)
            table.add_column("nom", justify="center", style="cyan", no_wrap=True)
            table.add_column("lieu", justify="center", style="cyan", no_wrap=True)
            table.add_column("date_debut", justify="center", style="cyan", no_wrap=True)
            table.add_column("date_fin", justify="center", style="cyan", no_wrap=True)
            table.add_column("nbr_tour", justify="center", style="cyan", no_wrap=True)
            table.add_column("nbr_manche", justify="center", style="cyan", no_wrap=True)
            table.add_column("liste_joueurs", justify="center", style="cyan", no_wrap=True)
            table.add_column("time", justify="center", style="cyan", no_wrap=True)
            table.add_column("description", justify="center", style="cyan", no_wrap=True)
            

            for tournament in self.controller_data.get_tournament_list():
                table.add_row(
                    str(tournament["id"]),
                    str(tournament["name"]),
                    str(tournament["location"]),
                    str(tournament["tournament_date_begin"]),
                    str(tournament["tournament_date_end"]),
                    str(tournament["number_of_turn"]),
                    str(tournament["number_of_round"]),
                    str(tournament["players_list"]),
                    str(tournament["time_controller_choice"]),
                    str(tournament["description"]),
                )
                
            console = Console()
            console.print(table)
            self.console.print(
            "[italic]\n\nAppuyez sur [/italic]"
            "[bold green]'o'[/bold green][italic] pour revenir au menu ou [/italic][bold green]'q'[/bold green][italic]"
            " pour quitter[/italic]\n\n"
            )
            while True:
                response = input("Reponse (o / q): ")
                if response.lower() != "q" and response.lower() != "o":
                    self.console.print(self._return_msg_error("wrong_input_choice_to_save"))
                elif response.lower() == "o":
                    self.console.print("[bold]vous allez être redirigé vers le menu principal.[/bold]")
                    self._clear_screen(1)
                    return self.display_main_menu()
                elif response.lower() == "q":
                    self.console.print("[bold]Le programme va maintenant se terminer, à très bientôt.\n[/bold]")
                    self._clear_screen(1)
                    return self._exit(0)
        else:
            self.console.print(self._return_msg_error("no_tournament_created"))
            self._clear_screen(1)
            return self.display_create_tournament_menu()
            

    def display_create_player_menu(self):
        """display_create_player_menu
        display player creation menu and title
        loop as long as the entries are erroneous
        Returns:
            dict: player data
        """
        self._clear_screen(0)


Menu()
