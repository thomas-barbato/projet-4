"""import"""
from .validation import display_error, check_date_format, check_birth_date_format
from .screen_and_sys_func import clear_screen
from views.menu import TournamentMenu
from controllers.player_controller import PlayerController
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import re


class CreatePlayer:
    def __init__(self):
        self.console = Console()
        self.first_name: str = None
        self.last_name: str = None
        self.date_of_birth: str = None
        self.gender: str = None
        self.ranking: int = None
        self.score: float = 0.0
        self.id = 1

    def __call__(self):
        self.display_player_create_menu()

    def display_player_create_menu(self):
        """display_create_tournament_menu
        display tournament creation menu and title
        loop as long as the entries are erroneous
        Returns:
            dict : tournament data
        """
        clear_screen(0)
        self.console.print(
            "[bold][italic yellow]INSCRIRE UN NOUVEAU JOUEUR[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        self.display_player_first_name()
        self.display_player_last_name()
        self.display_player_date_of_birth()
        self.display_player_gender()
        self.display_player_ranking()
        self.display_player_informations()
        self.display_confirm_player_save()

    def display_player_continue(self):
        clear_screen(0)
        self.console.print(
            "[bold]\nBienvenue dans le menu d'inscription d'un nouveau joueur.[/bold]"
            "[bold]\nVeuillez remplire correctement les informations suivantes:\n[/bold]"
            "[italic]Appuyez sur [/italic]"
            "[bold green]'o'[/bold green] [italic] pour continuer ou [/italic][bold green]'n'[/bold green][italic]"
            " pour revenir au menu principal[/italic]\n\n"
        )
        response: str = input("Continuer (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_continue"))
            clear_screen(1)
            return self.display_player_continue()
        elif response.lower() == "o":
            return self.display_player_create_menu()
        elif response.lower() == "n":
            TournamentMenu().display_menu_choices()

    def display_player_last_name(self):
        try:
            self.last_name = input("\n\nNom du joueur: ")
            if not self.last_name:
                self.console.print(display_error("empty_field"))
                return self.display_player_last_name()
            else:
                return self.last_name
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.display_player_last_name()

    def display_player_first_name(self):
        try:
            self.first_name = input("\n\nPrenom du joueur: ")
            if not self.first_name:
                self.console.print(display_error("empty_field"))
                return self.display_player_first_name()
            else:
                return self.first_name
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.display_player_first_name()

    def display_player_date_of_birth(self):
        try:
            self.date_of_birth = input("\n\nDate de naissance: ")
            if check_birth_date_format(self.date_of_birth) is False:
                self.console.print(display_error("birth_date_format"))
                return self.display_player_date_of_birth()
            else:
                return self.date_of_birth
        except ValueError:
            self.console.print(display_error("birth_date_format"))
            return self.display_player_date_of_birth()

    def display_player_gender(self):
        try:
            self.gender = input("\n\nSexe du joueur (homme / femme): ")
            if self.gender.lower() not in ["homme", "femme"]:
                self.console.print(display_error("gender"))
                return self.display_player_gender()
            else:
                return self.gender
        except ValueError:
            self.console.print(display_error("gender"))
            return self.display_player_gender()

    def display_player_ranking(self):
        self.ranking = input("\n\nRang du joueur: ")
        if self.ranking != "":
            if not (self.ranking.isdigit() and int(self.ranking) >= 0):
                self.console.print(display_error("wrong_turn_type_entry"))
                return self.display_player_ranking()
            else:
                return int(self.ranking)
        else:
            # default value
            self.ranking = 0

    def display_player_informations(self):
        """display_save_tournament
        save tornament in database
        """
        clear_screen(1)
        self.console.print(
            "[bold][italic yellow]CONFIRMER L'INSCRIPTION DE VOTRE JOUEUR[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        print(
            "[bold]\nDernière étape avant la création d'inscrire votre joueur[/bold]"
            "[bold] Veuillez vérifier que les informations entrées sont correctes.\n[/bold]"
            "[italic]Appuyez sur [/italic]"
            "[bold green]'o'[/bold green][italic] pour sauvegarder ou [/italic][bold green]'n'[/bold green][italic]"
            "[italic]pour annuler et revenir au menu principal[/italic]\n\n"
        )

        print(
            Panel.fit(
                "[bold]Vos informations[/bold]\n\n"
                f"[bold green]Nom:[/bold green] [bold]{self.last_name}[/bold]\n"
                f"[bold green]Prénom:[/bold green] [bold]{self.first_name}[/bold]\n"
                f"[bold green]Date de naissance:[/bold green] [bold]{self.date_of_birth}[/bold]\n"
                f"[bold green]Sexe:[/bold green] [bold]{self.gender}[/bold]\n"
                f"[bold green]Rang:[/bold green] [bold]{self.ranking}[/bold]\n",
                border_style="red",
            )
        )

    def display_confirm_player_save(self):
        response = input("Confirmez les informations à sauvegarder (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_confirm"))
            return self.display_confirm_player_save()
        else:
            if response.lower() == "o":
                player_controller_data = PlayerController()
                player_controller_data.save(
                    [
                        self.first_name,
                        self.last_name,
                        self.date_of_birth,
                        self.gender,
                        self.ranking,
                        self.score,
                        self.id,
                    ]
                )
                self.console.print("[bold]Sauvegarde terminée...[/bold]")
                clear_screen(1)
                self.display_confirm_create_another_player()
            elif response.lower() == "n":
                self.console.print(
                    "\n[bold]Création annulée,[/bold]" "[bold]vous allez être redirigé vers le menu principal.[/bold]"
                )
                clear_screen(1)
                TournamentMenu().display_menu_choices()

    def display_confirm_create_another_player(self):
        response = input("Inscrire un nouveau joueur ? (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_confirm"))
            return self.display_confirm_player_save()
        else:
            if response.lower() == "o":
                clear_screen(1)
                self.display_player_create_menu()
            elif response.lower() == "n":
                self.console.print(
                    "\n[bold]Création annulée,[/bold]" "[bold]vous allez être redirigé vers le menu principal.[/bold]"
                )
                clear_screen(1)
                TournamentMenu().display_menu_choices()
