"""Display main menu, used within main_controller"""
from rich import pretty, print
from rich.console import Console
from rich.panel import Panel

from .screen_and_sys_func import clear_screen
from .validation import display_error


class TournamentMenu:
    """_Menu_
    display frontend
    """

    def __init__(
        self,
    ):
        pretty.install()
        self.console = Console(width=100)

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

        print(
            Panel.fit(
                "[bold green]Menu:[/bold green]\n\n"
                "[bold green]1)[/bold green] [bold]Créer un nouveau tournoi[/bold]\n"
                "[bold green]2)[/bold green] [bold]Inscrire un nouveau joueur[/bold]\n"
                "[bold green]3)[/bold green] [bold]Consulter les tournois créés[/bold]\n"
                "[bold green]4)[/bold green] [bold]Consulter les joueurs inscrits[/bold]\n"
                "[bold green]5)[/bold green] [bold]Consulter les rapports de tournois[/bold]\n"
                "[bold green]6)[/bold green] [bold]Quitter[/bold]\n",
                border_style="red",
            )
        )

    def display_menu_choices(self):
        self.display_main_menu()
        menu_choices = input("Entrez votre choix: ")
        if menu_choices in ["1", "2", "3", "4", "5", "6"]:
            return menu_choices
        else:
            self.console.print(display_error("main_choice_value"))
            clear_screen(1)
            return self.display_menu_choices()
