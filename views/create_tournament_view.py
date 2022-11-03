"""import"""
from .validation import display_error, check_date_format
from .screen_and_sys_func import clear_screen
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import re


class CreateTournament:
    def __init__(self):
        self.console = Console()
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        
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
        self.pairing_round: tuple = ()

    def getter(self, index):
        return {
            "tournament_name": self.tournament_name,
            "location": self.location,
            "tournament_date_begin": self.tournament_date_begin,
            "tournament_date_end": self.tournament_date_end,
            "number_of_turn": self.number_of_turn,
            "number_of_round": self.number_of_round,
            "players_choice": self.players_choice,
            "time_controller_choice": self.time_controller_choice,
            "description": self.description,
        }[index]

    def tournament_data(self):
        return {
            "tournament_name": self.tournament_name,
            "location": self.location,
            "tournament_date_begin": self.tournament_date_begin,
            "tournament_date_end": self.tournament_date_end,
            "number_of_turn": self.number_of_turn,
            "number_of_round": self.number_of_round,
            "players_choice": self.players_choice,
            "time_controller_choice": self.time_controller_choice,
            "description": self.description,
            "base_pairing": self.pairing_round,
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
        self.display_number_of_turn()
        self.display_number_of_round()
        self.display_player_list()
        self.display_player_choice()
        self.display_time_controller_choice()
        self.display_description()
        
    def display_tournament_continue(self):
        self.console.print(
            "[bold]\nBienvenue dans le menu de création d'un nouveau tournoi.[/bold]"
            "[bold]\nVeuillez remplire correctement les informations suivantes:\n[/bold]"
            "[italic]Appuyez sur [/italic]"
            "[bold green]'o'[/bold green] [italic] pour continuer ou [/italic][bold green]'n'[/bold green][italic]"
            " pour revenir au menu principal[/italic]\n\n"
        )
        response: str = input("Continuer (o/n): ")
        if response.lower() != "n" and response.lower() != "o":
            self.console.print(display_error("wrong_input_choice_to_continue"))
            clear_screen(1)
            return self.display_tournament_continue()
        elif response.lower() == "o":
            return self.display_create_menu()
        elif response.lower() == "n":
            return False

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

    def display_number_of_turn(self):
        self.number_of_turn = input("\nTours par manche (4 par défaut si laissé vide): ")
        if self.number_of_turn != "":
            if not (self.number_of_turn.isdigit() and int(self.number_of_turn) > 0):
                self.console.print(display_error("wrong_turn_type_entry"))
                return self.display_number_of_turn()
            else:
                return int(self.number_of_turn)
        else:
            # default value
            self.number_of_turn = 4

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
        if len(self.player_controller.get_players_list()) >= 8:
            table = Table(title="\n\n[bold]Liste des joueurs à inscrire à ce tournoi[/bold]\n")
            table.add_column("Id", justify="center", style="cyan", no_wrap=True)
            table.add_column("Nom", justify="center", style="white", no_wrap=True)
            table.add_column("Prenom", justify="center", style="white", no_wrap=True)
            table.add_column("Rank", justify="center", style="green", no_wrap=True)
            table.add_column("Score", justify="center", style="green", no_wrap=True)

            for player in self.player_controller.get_players_list():
                table.add_row(
                    str(player["id"]),
                    str(player["last_name"]),
                    str(player["first_name"]),
                    str(player["ranking"]),
                    str(player["score"]),
                )
            self.console.print(table)

        elif (
            len(self.player_controller.get_players_list()) <= 8 and len(self.player_controller.get_players_list()) > 0
        ):
            self.console.print(display_error("too_few_player_created"))
            # redirection here...
        else:
            self.console.print(display_error("no_player_created"))
            # redirection here...

    def display_player_choice(self):
        self.console.print(
            "\n\n[bold]Veuillez selectionner [blue]8[/blue] joueurs parmis la liste présente[/bold]",
            "[bold]en entrant leurs numéro [blue]ID[/blue] séparés par un espace[/bold]",
        )
        self.players_choice = input("Entrez votre selection: ")
        # delete every character is not a number
        research = re.sub(r"[^0-9]", ",", self.players_choice)
        # store it in list
        self.players_choice = [int(nb) for nb in research.split(",") if nb != ""]
        if len(self.players_choice) < 8 or len(self.players_choice) > 8:
            self.console.print(display_error("wrong_player_number_selected"))
            return self.display_player_choice()
        else:
            return self.players_choice

    def display_time_controller_choice(self):
        try:
            timeController = TournamentController()
            self.time_controller_choice = input("Tournée (blitz / bullet / coup_rapide): ")
            if (
                self.time_controller_choice != ''
                and timeController.check_enum_status(self.time_controller_choice) is False
                or not self.time_controller_choice
            ):
                self.console.print(display_error("time_controller_field"))
                return self.display_time_controller_choice()
            else:
                return self.time_controller_choice
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.display_time_controller_choice()

    def display_description(self):
        try:
            self.description = input("\nDescription du tournois: ")
            if not self.description:
                self.console.print(display_error("empty_field"))
                return self.display_description()
            else:
                return self.description
        except ValueError:
            self.console.print(display_error("empty_field"))
            return self.display_description()

    def display_tournament_informations(self):
        """display_save_tournament
        save tornament in database
        """
        player_controller = PlayerController()

        clear_screen(1)
        self.console.print(
            "[bold][italic yellow]CONFIRMER LA CREATION DE VOTRE TOURNOI[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        print(
            "[bold]\nDernière étape avant la création de votre nouveau tournois[/bold]"
            "[bold] Veuillez vérifier que les informations entrées sont correctes.\n[/bold]"
            "[italic]Appuyez sur [/italic]"
            "[bold green]'o'[/bold green][italic] pour sauvegarder ou [/italic][bold green]'n'[/bold green][italic]"
            "[italic]pour annuler et revenir au menu principal[/italic]\n\n"
        )

        print(
            Panel.fit(
                "[bold]Vos informations[/bold]\n\n"
                f"[bold green]Nom du tournoi:[/bold green] [bold]{self.tournament_data()['tournament_name']}[/bold]\n"
                f"[bold green]Lieu du tournoi:[/bold green] [bold]{self.tournament_data()['location']}[/bold]\n"
                f"[bold green]date début:[/bold green]"
                f"[bold]{self.tournament_data()['tournament_date_begin']}[/bold]\n"
                f"[bold green]date fin:[/bold green] [bold]{self.tournament_data()['tournament_date_end']}[/bold]\n"
                f"[bold green]tour par ronde:[/bold green] [bold]{self.tournament_data()['number_of_turn']}[/bold]\n"
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
            selected_players_table.add_column("rank", justify="center", style="green", no_wrap=True)
            for i in range(0, len(player_controller.get_players_list())):
                if player_controller.get_players_list()[i]["id"] in self.players_choice:
                    selected_players_table.add_row(
                        str(player_controller.get_players_list()[i]["id"]),
                        str(player_controller.get_players_list()[i]["first_name"]),
                        str(player_controller.get_players_list()[i]["last_name"]),
                        str(player_controller.get_players_list()[i]["ranking"]),
                    )

            self.console.print(selected_players_table)

    def display_confirm_tournament_save(self):
        response = input("Confirmez les informations à sauvegarder (o/n): ")
        if response.lower() != "n" and response.lower() != "o":
            self.console.print(display_error("wrong_input_choice_to_confirm"))
            return self.display_confirm_tournament_save()
        else:
            if response.lower() == "o":

                
                self.pairing_round = TournamentController(self.tournament_data()).set_pairing_first_round(self.players_choice)
                tournament_controller_data = TournamentController(self.tournament_data())
                tournament_controller_data.save()
                self.console.print("[bold]Sauvegarde terminée...[/bold]")
                clear_screen(1)
                return self.display_pairing_and_tournament()
            elif response.lower() == "n":
                self.console.print(
                    "\n[bold]Création annulée,[/bold]" "[bold]vous allez être redirigé vers le menu principal.[/bold]"
                )
                clear_screen(1)
            return response.lower()

    def display_pairing_and_tournament(self):
        self.console.print(
            "[bold][italic yellow]VOTRE TOURNOIS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        # DO : save only last result.
        if len(self.player_controller.get_players_list()) >= 8:
            pairing_table = Table(title="\n\n[bold]Paires de début de tournoi[/bold]\n")
            pairing_table.add_column("Numéro Equipe", justify="center", style="white", no_wrap=True)
            pairing_table.add_column("Competiteur 1", justify="center", style="white", no_wrap=True)
            pairing_table.add_column("Competiteur 2", justify="center", style="white", no_wrap=True)
            for i in range(0, len(self.pairing_round)):
                pairing_table.add_row(
                    f"{i}",
                    f'{self.pairing_round[i][0]["last_name"]}',
                    f'{self.pairing_round[i][1]["last_name"]}',
                )
            self.console.print(pairing_table)
            self.display_tournament_begin()
    
    def display_tournament_begin(self):
        self.console.print(f"\n[bold]Le tournoi va se dérouler en {self.number_of_turn} tours.[/bold]\n"
                           "[bold]Chaque équipes vont s'affronter:[/bold]\n"
                           "un match gagné = 1 point\n"
                           "un match perdu = 0 point\n"
                           "un match nul = 0.5 pour les deux participants.")
        for i in range(1,self.number_of_round+1):
            choice = 0
            if i == 1:
                self.console.print(f"\n\n[bold]Match {i}:[/bold]\n")
                
            else: 
                pairing_table = Table(title="\n\n[bold]Match {i}:[/bold]\n")
                pairing_table.add_column("Numéro Equipe", justify="center", style="white", no_wrap=True)
                pairing_table.add_column("Competiteur 1", justify="center", style="white", no_wrap=True)
                pairing_table.add_column("Competiteur 2", justify="center", style="white", no_wrap=True)
                for i in range(0, len(self.pairing_round)):
                    pairing_table.add_row(
                        f"{i}",
                        f'{self.pairing_round[i][0]["last_name"]}',
                        f'{self.pairing_round[i][1]["last_name"]}',
                    )
                self.console.print(pairing_table)
            for paire in self.pairing_round:
                self.console.print("[bold]Selectionnez la valeur correcte:\n[/bold]"
                                   f"[italic green]1)[/italic green] {paire[0]['last_name']}\n"
                                   f"[italic green]2)[/italic green] {paire[1]['last_name']}\n"
                                   "[italic green]3)[/italic green] Match nul\n")
                
                while True:
                    choice = input("Résultat: ")
                    if not choice or choice not in ["1","2","3"]:
                        self.console.print(display_error("wrong_match_result_input"))
                    else:
                        if choice == "1":
                            self.console.print(f"[bold]Le competiteur [/bold]" 
                                               f"[bold]{paire[0]['last_name']} prend 1 point[/bold]")
                            paire[0]['score'] = ( paire[0]['score'] + 1.0 )
                        elif choice == "2":
                            self.console.print(f"[bold]Le competiteur [/bold]" 
                                               f"[bold]{paire[1]['last_name']} prend 1 point[/bold]")
                            paire[1]['score'] = ( paire[1]['score'] + 1.0 )
                        elif choice == "3":
                            self.console.print(f"[bold]Les competiteurs {paire[0]['last_name']}[/bold]"
                                                "[bold] et [/bold]"
                                                f"[bold]{paire[1]['last_name']} prennent 0.5 point[/bold]")
                            paire[0]['score'] = ( paire[0]['score'] + 0.5 ) 
                            paire[1]['score'] = ( paire[1]['score'] + 0.5 ) 
                        break
                print(self.pairing_round)
                self.player_controller.update_score(self.pairing_round)
                self.pairing_round = TournamentController(self.tournament_data()).set_pairing_next_round(self.players_choice)
            self.console.print(f"\n\n[bold]Match {i} Terminé[/bold]\n")
            
