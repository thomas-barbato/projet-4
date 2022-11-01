from controllers.screen_and_sys_func import *
from controllers.validation import display_error
from rich import pretty, print
from rich.console import Console
from rich.panel import Panel

console = Console()


def display_menu_choices():
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
            return menu_choices
        else:
            console.print(display_error("main_choice_value"))
            clear_screen(1)
            display_menu_choices()
    except ValueError:
        console.print(display_error("main_choice_type"))
        clear_screen(1)
        display_menu_choices()
