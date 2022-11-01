"""import"""
from controllers.validation import display_error, check_date_format
from controllers.screen_and_sys_func import clear_screen
from controllers.engine import Controller
from models.tables import Tournament
from rich import pretty, print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import re


console = Console()
controller_data: Controller = Controller()


def display_tournament_continue():
    response: str = input("Continuer (o/n): ")
    if response.lower() != "n" and response.lower() != "o":
        console.print(display_error("wrong_input_choice_to_continue"))
        return display_tournament_continue()
    elif response.lower() == "o":
        return response.lower()
    elif response.lower() == "n":
        return response.lower()


def display_tournament_name():
    try:
        tournament_name = input("\n\nNom du tournoi: ")
        if not tournament_name:
            console.print(display_error("empty_field"))
            return display_tournament_name()
        else:
            return tournament_name
    except ValueError:
        console.print(display_error("empty_field"))
        return display_tournament_name()


def display_location_tournament():
    try:
        location = input("\nLieu du tournoi: ")
        if not location:
            console.print(display_error("empty_field"))
            return display_location_tournament()
        else:
            return location
    except ValueError:
        console.print(display_error("empty_field"))
        return display_location_tournament()


def display_tournament_date(temp):
    if temp == "begin":
        temp_input = "\nDate et heure de début du tournoi (jj-mm-aaaa hh:mm): "
    else:
        temp_input = "\nDate et heure de fin du tournoi (jj-mm-aaaa hh:mm): "
    try:
        tournament_date = input(temp_input)
        if check_date_format(tournament_date) is False:
            console.print(display_error("date_format"))
            return display_tournament_date(temp)
        else:
            return tournament_date
    except ValueError:
        console.print(display_error("date_format"))
        return display_tournament_date(temp)


def display_number_of_turn():
    number_of_turn = input("\nTours par manche (4 par défaut si laissé vide): ")
    if number_of_turn != "":
        if not (number_of_turn.isdigit() and int(number_of_turn) > 0):
            console.print(display_error("wrong_turn_type_entry"))
            return display_number_of_turn()
        else:
            return int(number_of_turn)
    else:
        # default value
        return 4


def display_number_of_round():
    number_of_round = input("\nNombre de ronde (3 par défaut si laissé vide): ")
    if number_of_round != "":
        if not (number_of_round.isdigit() and int(number_of_round) > 0):
            console.print(display_error("wrong_turn_type_entry"))
            return display_number_of_round()
        else:
            return int(number_of_round)
    else:
        # default value
        return 3


def display_player_list():
    if len(controller_data.get_players_list()) >= 8:
        table = Table(title="\n\n[bold]Liste des joueurs à inscrire à ce tournoi[/bold]\n")
        table.add_column("Id", justify="center", style="cyan", no_wrap=True)
        table.add_column("Nom", justify="center", style="white", no_wrap=True)
        table.add_column("Prenom", justify="center", style="white", no_wrap=True)
        table.add_column("Rank", justify="center", style="green", no_wrap=True)

        for player in controller_data.get_players_list():
            table.add_row(
                str(player["id"]),
                str(player["last_name"]),
                str(player["first_name"]),
                str(player["ranking"]),
            )
        console = Console()
        console.print(table)

    elif len(controller_data.get_players_list()) <= 8 and len(controller_data.get_players_list()) > 0:
        console.print(display_error("too_few_player_created"))
        # redirection here...
    else:
        console.print(display_error("no_player_created"))
        # redirection here...


def display_player_choice():
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
        console.print(display_error("wrong_player_number_selected"))
        return display_player_choice()
    else:
        return players_list


def display_time_controller_choice():
    try:
        time_controller_choice = input("Tournée (blitz / bullet / coup_rapide): ")
        if (
            time_controller_choice
            and controller_data.check_enum_status(time_controller_choice) is False
            or not time_controller_choice
        ):
            console.print(display_error("time_controller_field"))
            return display_time_controller_choice()
        else:
            return time_controller_choice
    except ValueError:
        console.print(display_error("empty_field"))
        return display_time_controller_choice()


def display_description():
    try:
        description = input("\nDescription du tournois: ")
        if not description:
            console.print(display_error("empty_field"))
            return display_description()
        else:
            return description
    except ValueError:
        console.print(display_error("empty_field"))
        return display_description()


def display_confirm_tournament_choice(tournament_data):
    response = input("Confirmez les informations (o/n): ")
    if response.lower() != "n" and response.lower() != "o":
        console.print(display_error("wrong_input_choice_to_confirm"))
        return display_confirm_tournament_choice(tournament_data)
    else:
        if response.lower() == "o":
            clear_screen(1)
        elif response.lower() == "n":
            console.print(
                "\n[bold]Création annulée,[/bold]" "[bold]vous allez être redirigé vers le menu principal.[/bold]"
            )
            clear_screen(1)
        return response.lower()


def display_save_tournament_choice(tournament_data):
    response = input("sauvegarder (o/n): ")
    if response.lower() != "n" and response.lower() != "o":
        console.print(display_error("wrong_input_choice_to_save"))
        return display_save_tournament_choice(tournament_data)
    else:
        if response.lower() == "o":
            tournament = Tournament(tournament_data)
            tournament.save()
            console.print(
                "\n[bold]Le tournoi a été correctement sauvegardé,[/bold]"
                "[bold]vous allez être redirigé vers le menu principal.[/bold]"
            )
            clear_screen(1)
        elif response.lower() == "n":
            console.print(
                "\n[bold]Sauvegarde annulée,[/bold]" "[bold]vous allez être redirigé vers le menu principal.[/bold]"
            )
            clear_screen(1)
        return response.lower()
