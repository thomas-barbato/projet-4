"""import"""
from .validation import display_error, check_date_format
from .screen_and_sys_func import clear_screen
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from .menu import TournamentMenu
from models.tables import Tournament, Player, Match, Tour
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import re


class Playmatch:
    def __init__(self, data, list_of_completed_match=[]):
        self.console = Console()
        self.pairing: tuple = ()
        self.player_controller: PlayerController = PlayerController()
        self.match_model: Match = Match()
        self.tour_model: Tour = Tour()
        self.time_begin: str = ""
        self.time_end: str = ""
        self.list_of_completed_match: list = list_of_completed_match
        self.matchs_list_per_tour: list = []
        self.new_tour: list = []
        # set data in Tournament instance
        self.tournament_object: Tournament = Tournament().unset_data(data)
        # allow editing.
        self.tournament_object_editable_data: Tournament = self.tournament_object.set_data()

    def display_pairing(self, round_number):

        pairing_table = Table(title=f"\n\n[bold]Paires tour {self.tour_model.NUMBER_OF_TOUR}[/bold]\n")
        pairing_table.add_column("Numéro Equipe", justify="center", style="white", no_wrap=True)
        pairing_table.add_column("Competiteur 1", justify="center", style="white", no_wrap=True)
        pairing_table.add_column("Competiteur 2", justify="center", style="white", no_wrap=True)
        for i in range(0, len(self.pairing)):
            pairing_table.add_row(
                f"{i}",
                f'{self.pairing[i][0]["first_name"]} {self.pairing[i][0]["last_name"]}',
                f'{self.pairing[i][1]["first_name"]} {self.pairing[i][1]["last_name"]}',
            )
        self.console.print(pairing_table)

    def start_chronometer(self):
        response: str = input("Lancer le chronomètre ? (o/n): ")
        if response.lower() != "n" and response.lower() != "o":
            self.console.print(display_error("wrong_input_choice_to_continue"))
            self.start_chronometer()
        elif response.lower() == "o":
            self.time_begin = self.tour_model.get_time_now()
        elif response.lower() == "n":
            self.start_chronometer()

    def end_chronometer(self):
        response: str = input("Arrêter le chronomètre ? (o/n): ")
        if response.lower() != "n" and response.lower() != "o":
            self.console.print(display_error("wrong_input_choice_to_continue"))
            self.end_chronometer()
        elif response.lower() == "o":
            self.time_end = self.tour_model.get_time_now()
        elif response.lower() == "n":
            self.end_chronometer()

    def save_tournament_current_tour(self, tournament_instance, tour_instance):
        response: str = input("Voulez-vous sauvegarder et quitter la manche en cours ? (o/n): ")
        if response.lower() != "n" and response.lower() != "o":
            self.console.print(display_error("wrong_input_choice_to_continue"))
        elif response.lower() == "o":
            TournamentController().save_current_tour(tournament_instance, tour_instance)
            self.console.print("[bold]Sauvegarde terminée...[/bold]")
            self.console.print("\n[bold]vous allez être redirigé vers le menu principal.[/bold]")
            return TournamentMenu().display_menu_choices()

    def select_result(self):
        response: str = input("Résultat: ")
        if response not in ["1", "2", "3"]:
            self.console.print(display_error("wrong_match_result_input"))
            return self.select_result()
        else:
            return response

    def display_tournament_begin(self):
        if self.tour_model.NUMBER_OF_TOUR == 1:
            self.pairing = self.player_controller.sort_players_by_rank(self.tournament_object.players_choice)

        for i in range(0, len(self.pairing)):
            match = Match(
                self.pairing[i][0], self.pairing[i][1], self.pairing[i][0]["score"], self.pairing[i][1]["score"]
            )
            self.matchs_list_per_tour.append(match)
        # change itterator value to
        # use unplayed tour.
        # check if round_ids is not empty ,
        # if it's empty : take 1
        # else : number of round - len of round_ids
        count_tour_already_completed = (
            self.tournament_object_editable_data["number_of_round"]
            - len(self.tournament_object_editable_data["round_ids"])
            if len(self.tournament_object_editable_data["round_ids"]) > 0
            else self.tournament_object_editable_data["number_of_round"]
        )
        # delete or not, i will see.
        self.tour_model.NUMBER_OF_TOUR = len(self.tournament_object_editable_data["round_ids"]) if len(self.tournament_object_editable_data["round_ids"]) > 0 else 1
        print(self.tour_model.NUMBER_OF_TOUR)
        for _ in range(1, count_tour_already_completed + 1):
            self.display_pairing(self.tour_model.NUMBER_OF_TOUR)
            self.console.print(
                f"\n[bold]Le tournoi va se dérouler en {self.tournament_object_editable_data['number_of_round']} tours.[/bold]\n"
                "[bold]Attribution des scores:[/bold]\n"
                "un match gagné = 1 point\n"
                "un match perdu = 0 point\n"
                "un match nul = 0.5 pour les deux participants.\n"
            )
            self.start_chronometer()
            self.end_chronometer()
            for match in self.matchs_list_per_tour:
                while True:
                    self.console.print(
                        "[bold]Selectionnez la valeur correcte:\n[/bold]"
                        f"[italic green]1)[/italic green] {match.player_1['last_name']}\n"
                        f"[italic green]2)[/italic green] {match.player_2['last_name']}\n"
                        "[italic green]3)[/italic green] Match nul\n"
                    )
                    choice = self.select_result()
                    if choice == "1":
                        self.console.print(
                            f"\n[bold]Le competiteur [/bold]"
                            f"[bold]{match.player_1['last_name']} prend 1 point[/bold]"
                        )
                        match.score_player_1 += 1.0
                    elif choice == "2":
                        self.console.print(
                            f"\n[bold]Le competiteur [/bold]"
                            f"[bold]{match.player_2['last_name']} prend 1 point[/bold]"
                        )
                        match.score_player_2 += 1.0
                    elif choice == "3":
                        self.console.print(
                            f"\n[bold]Les competiteurs {match.player_1['last_name']}[/bold]"
                            "[bold] et [/bold]"
                            f"[bold]{match.player_2['last_name']} prennent 0.5 point[/bold]"
                        )
                        match.score_player_1 += 0.5
                        match.score_player_2 += 0.5
                    break

                self.list_of_completed_match.append(
                    [
                        [match.player_1["id"], match.score_player_1],
                        [match.player_2["id"], match.score_player_2],
                    ]
                )

                self.match_model.up_match_number()
            self.new_tour = Tour(self.time_begin, self.time_end, self.list_of_completed_match)
            self.save_tournament_current_tour(self.tournament_object, self.new_tour)
            # reset list
            self.pairing = self.player_controller.sort_players_by_score(self.list_of_completed_match)
            self.list_of_completed_match = []
            TournamentController().save_current_tour(self.tournament_object, self.new_tour)
            self.tour_model.up_turn_number()
