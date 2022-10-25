import os
import sys

PROJECT_CWD = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1])
sys.path.append(PROJECT_CWD)
sys.path.append(os.path.join(PROJECT_CWD, "controllers"))

from numpy import number
from rich import (
    print,
)
from rich import (
    pretty,
)
from rich.console import (
    Console,
)
from rich.align import (
    Align,
)
from rich.text import (
    Text,
)
from rich.panel import (
    Panel,
)
from rich.console import (
    Console,
)
from rich.progress import Progress
from rich.progress import track
import os
from time import sleep
import datetime



class Menu:
    def __init__(
        self,
    ):
        pretty.install()
        self.console = Console(width=100)
        self.menu_choices: int = 0

    def __clear_screen(self, sleep_val: int =0):
        sleep(sleep_val)
        return os.system("cls")

    def __exit(self, sleep_val: int =0):
        sleep(sleep_val)
        return os.system("exit")

    def __return_msg_error(self, category: str):
        if category == "main_choice_value":
            return self.console.print(
                "[italic red]Veuillez entrer une valeur numérique comprise entre 1 et 5...\n[/italic red]"
            )
        elif category == "main_choice_type":
            return self.console.print("[italic red]Veuillez entrer une valeur numérique...\n[/italic red]")
        elif category == "wrong_input_choice_to_continue":
            self.console.print(
                "[italic red]Appuyez sur [/italic red][bold]'o'[/bold][italic red] pour continuer ou"
                "[/italic red][bold]'n'[/bold][italic red] pour revenir au menu principal[/italic red]"
            )
        elif category == "empty_field":
            return self.console.print("[italic red]Veuillez renseigner ce champ[/italic red]")
        elif category == "date_format":
            self.console.print(
                "[italic red]Format de date incorrect, format attendu: jj-mm-aaaa hh:mm\nExemple: [bold]10-09-2022 10:30[/bold][/italic red]"
            )
        elif category == "wrong_turn_type_entry":
            self.console.print(
                "[italic red]Veuillez entrer une valeur correcte, format attendu: [bold]un entier positif superieur à 0[/bold][/italic red]"
            )

    def __check_date_format(self, date: str):
        try:
            datetime.datetime.strptime(date, "%d-%m-%Y %H:%M")
            return True
        except ValueError:
            return False

    def display_main_menu_title(
        self,
    ):
        """display_main_menu_title
        Returns:
            nothing
        """
        return self.console.print(
            "[bold][italic yellow]GESTION TOURNOIS D'ECHECS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )

    def display_create_tournament_menu_title(self):
        """display_main_menu_title
        Returns:
            nothing
        """
        return self.console.print(
            "[bold][italic yellow]CREER UN NOUVEAU TOURNOI[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )

    def display_main_menu(self):
        """display_main_menu
        display main menu title and main menu
        loop as long as the entries are erroneous
        and redirect to selected choice view
        Returns:
            method
        """
        while True:
            self.display_main_menu_title()
            self.menu_choices = 0
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
                if self.menu_choices >= 1 and self.menu_choices <= 5:
                    break
                else:
                    self.__return_msg_error("main_choice_value")
                    self.__clear_screen(1)
            except ValueError:
                self.__return_msg_error("main_choice_type")
                self.__clear_screen(1)
        if self.menu_choices == 1:
            return self.display_create_tournament_menu()
        elif self.menu_choices == 5:
            print("[italic red]Le programme va maintenant se terminer, à très bientôt.\n[/italic red]")
            self.__clear_screen(1)
            return self.__exit(1)

    def get_main_menu_choices(self):
        return self.menu_choices

    def display_create_tournament_menu(self):
        """display_create_tournament_menu
        display tournament creation menu and title
        loop as long as the entries are erroneous
        Returns:
            int: _self.menu_choices
        """
        self.__clear_screen(0)
        continue_displaying_start_choice = True
        self.display_create_tournament_menu_title()
        self.console.print(
            "[bold]\nBienvenue dans le menu de création d'un nouveau tournoi, veuillez remplire correctement les informations suivantes:\n[/bold]"
            "[italic]Appuyez sur [/italic][bold]'o'[/bold][italic] pour continuer ou [/italic][bold]'n'[/bold][italic] pour revenir au menu principal[/italic]\n\n"
        )
        while continue_displaying_start_choice is True:
            response = input("Continuer (o/n): ")
            if response.lower() == "n":
                self.__clear_screen(0)
                return self.display_main_menu()
            elif response.lower() == "o":
                continue_displaying_start_choice = False
            else:
                self.__return_msg_error("wrong_input_choice_to_continue")

        while True:
            try:
                tournament_name = input("\nNom du tournoi: ")
                if tournament_name:
                    break
                else:
                    self.__return_msg_error("empty_field")
            except ValueError as e:
                self.console.print(self.__return_msg_error("empty_field"))

        while True:
            try:
                location = input("lieu du tournoi: ")
                if location:
                    break
                else:
                    self.__return_msg_error("empty_field")
            except ValueError as e:
                self.__return_msg_error("empty_field")

        while True:
            try:
                date = input("date et heure du tournoi (jj-mm-aaaa hh:mm): ")
                if self.__check_date_format(date) is True:
                    break
                else:
                    self.__return_msg_error("date_format")
            except ValueError:
                self.__return_msg_error("date_format")

        while True:
            number_of_turn = input("tours par manche (4 par défaut si laissé vide): ")
            if number_of_turn != '':
                if number_of_turn.isdigit() and int(number_of_turn) > 0:
                    break
                else:
                    self.__return_msg_error("wrong_turn_type_entry")
            else:
                number_of_turn = 4
                break
        
        print(number_of_turn)
        


x = Menu()
x.display_main_menu()
print(x.get_main_menu_choices())