"""import"""
#sys.path.insert(1, os.path.join(sys.path[0], ".."))
from .create_tournament_view import CreateTournament
from .screen_and_sys_func import clear_screen, exit_to_console
from .validation import display_error
from rich import print, pretty
from rich.console import Console
from rich.panel import Panel


class TournamentMenu:
    """_Menu_
    display frontend
    """

    def __init__(
        self,
    ):
        pretty.install()
        self.console = Console(width=100)
        self.display_main_menu()

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
        self.display_menu_choices()

    def display_menu_choices(self):
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
            menu_choices = int(input("Entrez votre choix: "))
            if menu_choices in [1, 2, 3, 4, 5]:
                if menu_choices == 1:
                    createTournament = CreateTournament()
                    if createTournament.display_tournament_continue() is False:
                        return self.display_menu_choices()
                    if createTournament.display_confirm_tournament_save() == "n":
                        return self.display_menu_choices()
                elif menu_choices == 2:
                    pass
                elif menu_choices == 3:
                    pass
                elif menu_choices == 4:
                    pass
                elif menu_choices == 5:
                    self.console.print("[italic red]Le programme va maintenant se terminer, à bientot.[/italic red]")
                    exit_to_console(1)
            else:
                self.console.print(display_error("main_choice_value"))
                clear_screen(1)
                self.display_menu_choices()
        except ValueError:
            self.console.print(display_error("main_choice_type"))
            clear_screen(1)
            self.display_menu_choices()

    def display_create_player_menu(self):
        """display_create_player_menu
        display player creation menu and title
        loop as long as the entries are erroneous
        Returns:
            dict: player data
        """
        clear_screen(0)
