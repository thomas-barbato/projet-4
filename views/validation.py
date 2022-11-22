# TODO: Docstring should contain a description of the file containss
"""import"""
import datetime


def display_error(category: str):
    """_return_msg_error_
    Args:
        category (str): _description_
    show error msg.
    """
    return {
        "main_choice_value": "[italic red]Veuillez entrer une valeur numérique comprise entre 1 et 5\n[/italic red]\n",
        "main_choice_type": "[italic red]Veuillez entrer une valeur numérique...\n[/italic red]\n",
        "wrong_input_choice_to_continue": "[italic red]Appuyez sur [/italic red][bold]'o'[/bold][italic red]"
        " pour continuer ou [/italic red][bold green]'n'[/bold green][italic red]"
        "pour revenir au menu principal[/italic red]\n",
        "empty_field": "[italic red]Veuillez renseigner ce champ[/italic red]",
        "date_format": "[italic red]Format de date incorrect, format attendu: jj-mm-aaaa hh:mm\nExemple: "
        "[bold]10-09-2022 10:30[/bold][/italic red]\n",
        "birth_date_format": "[italic red]Format de date incorrect, format attendu: jj-mm-aaaa\nExemple: "
        "[bold]06-04-1980[/bold][/italic red]\n",
        "wrong_turn_type_entry": "[italic red]Veuillez entrer une valeur correcte, format attendu: "
        "[bold]un entier positif superieur à 0[/bold][/italic red]\n",
        "time_controller_field": "[italic red]Veuillez entrer une valeur correcte, choix attendu:"
        "[bold] blitz[/bold] ou [bold]bullet[/bold] ou [bold]coup_rapide[/bold][/italic red]\n",
        "no_player_created": "[italic red]\n\n[bold]Vous n'avez pas encore inscrit de joueur.[/bold][/italic red]"
        "\n\n[bold]Vous allez être redirigé vers la page d'inscription de nouveaux joueurs.[/bold]",
        "too_few_player_created": "[italic red]\n\nVeuillez inscrire au moins[bold] 8 joueurs[/bold][/italic red]"
        "[italic red] afin de pouvoir les assigner à un tournois[/italic red]"
        "\n\n[bold]Vous allez être redirigé vers la page d'inscription de nouveaux joueurs.[/bold]",
        "wrong_player_number_selected": "[italic red]Veuillez selectionner[bold] 8 joueurs [/bold]"
        "[bold]uniques et existants[/bold][/italic red]",
        "no_tournament_created": "[italic red][bold]\n\nVous n'avez pas encore créé de tournoi.[/bold][/italic red]"
        "\n\n[bold]Vous allez être redirigé vers la page de création de tournois.[/bold]",
        "wrong_input_choice_to_save": "[italic red]Appuyez sur [/italic red][bold]'o'[/bold]"
        "[italic red] pour sauvegarder ou"
        "[/italic red][bold green] 'n'[/bold green]"
        "[italic red] pour annuler et revenir au menu principal[/italic red]\n",
        "wrong_input_choice_to_confirm": "[italic red]Appuyez sur [/italic red][bold]'o'[/bold]"
        "[italic red] pour confirmer ou"
        "[/italic red][bold green] 'n'[/bold green]"
        "[italic red] pour annuler et revenir au menu principal[/italic red]\n",
        "wrong_match_result_input": "[italic red]Mauvais choix selectionné[/italic red]"
        "[italic red] veuillez entrer l'un des choix suivants: [/italic red]"
        "[bold red]1, 2[/bold red][italic red] ou [/italic red][bold red]3[/bold red]",
        "gender": "[italic red]Mauvais choix selectionné[/italic red]"
        "[italic red] veuillez entrer l'un des choix suivants: [/italic red]"
        "[bold red]homme[/bold red][italic red] ou [/italic red][bold red]femme[/bold red]",
        "tournament_id_unknown": "[italic red]Veuillez entrer une ID valide[/italic red]",
        "wrong_input_player_display_choice": "[italic red]Veuillez entrer une valeur correcte,[/italic red]"
        "[italic red] format attendu:\n[/italic red]"
        "[bold red]1[/bold red], [bold red]2[/bold red], [bold red]3[/bold red] ou [bold red]4[/bold red].",
        "wrong_input_report_display_choice": "[italic red]Veuillez entrer une valeur correcte,[/italic red]"
        "[italic red] format attendu:\n[/italic red]"
        "[bold red]1[/bold red], [bold red]2[/bold red] ou [bold red]3[/bold red].",
        "wrong_input_player_report_display_choice": "[italic red]Veuillez entrer une valeur correcte,[/italic red]"
        "[italic red] format attendu:\n[/italic red]"
        "[bold red]1[/bold red], [bold red]2[/bold red], [bold red]3[/bold red] ou [bold red]4[/bold red].",
    }[category]


def check_date_format(date: str):
    try:
        datetime.datetime.strptime(date, "%d-%m-%Y %H:%M")
        return True
    except ValueError:
        return False


def check_birth_date_format(date: str):
    try:
        datetime.datetime.strptime(date, "%d-%m-%Y")
        return True
    except ValueError:
        return False
