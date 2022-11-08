"""import"""
from .validation import display_error, check_date_format
from .screen_and_sys_func import clear_screen
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from models.tables import Tournament
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import re


class Playmatch:
    def __init__(self, data):
        self.console = Console()
        self.pairing_round = []
        # set data in Tournament instance
        self.tournament_object = Tournament().unset_data(data)
        # allow editing.
        self.tournament_object_update = self.tournament_object.set_data()

    def display_pairing(self):
        print(self.tournament_object)
        print(self.tournament_object.players_choice)

        self.tournament_object_update["location"] = "test2222"
        print(self.tournament_object_update)
        self.y = self.tournament_object.unset_data(self.tournament_object_update)
        # self.tournament_object.update(self.tournament_object_update)

        pairing_table = Table(title="\n\n[bold]Paires de début de tournoi[/bold]\n")
        pairing_table.add_column("Numéro Equipe", justify="center", style="white", no_wrap=True)
        pairing_table.add_column("Competiteur 1", justify="center", style="white", no_wrap=True)
        pairing_table.add_column("Competiteur 2", justify="center", style="white", no_wrap=True)
        for i in range(0, len(self.pairing_round)):
            print(self.pairing_round)
            pairing_table.add_row(
                f"{i}",
                f'{self.pairing_round[i][0]["last_name"]}',
                f'{self.pairing_round[i][1]["last_name"]}',
            )
        self.console.print(pairing_table)

    def display_tournament_begin(self):
        self.display_pairing()
        self.console.print(
            f"\n[bold]Le tournoi va se dérouler en {self.tournament_instance['number_of_round']} tours.[/bold]\n"
            "[bold]Chaque équipes vont s'affronter:[/bold]\n"
            "un match gagné = 1 point\n"
            "un match perdu = 0 point\n"
            "un match nul = 0.5 pour les deux participants."
        )
        for tour in range(1, self.tournament_instance["number_of_tour"] + 1):
            choice = 0
            if tour == 1:
                self.console.print(f"\n\n[bold]Match {tour}:[/bold]\n")

            else:
                pairing_table = Table(title="\n\n[bold]Match {tour}:[/bold]\n")
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
            # from tuple to list to allow editing
            self.pairing_round = list(self.pairing_round)
            for i in range(0, len(self.pairing_round)):
                self.console.print(
                    "[bold]Selectionnez la valeur correcte:\n[/bold]"
                    f"[italic green]1)[/italic green] {self.pairing_round[i][0]['last_name']}\n"
                    f"[italic green]2)[/italic green] {self.pairing_round[i][1]['last_name']}\n"
                    "[italic green]3)[/italic green] Match nul\n"
                )
                while True:
                    choice = input("Résultat: ")
                    if not choice or choice not in ["1", "2", "3"]:
                        self.console.print(display_error("wrong_match_result_input"))
                    else:
                        if choice == "1":
                            self.console.print(
                                f"[bold]Le competiteur [/bold]"
                                f"[bold]{self.pairing_round[i][0]['last_name']} prend 1 point[/bold]"
                            )
                            self.pairing_round[i][0]["score"] += 1.0
                        elif choice == "2":
                            self.console.print(
                                f"[bold]Le competiteur [/bold]"
                                f"[bold]{self.pairing_round[i][1]['last_name']} prend 1 point[/bold]"
                            )
                            self.pairing_round[i][1]["score"] += 1.0
                        elif choice == "3":
                            self.console.print(
                                f"[bold]Les competiteurs {self.pairing_round[i][0]['last_name']}[/bold]"
                                "[bold] et [/bold]"
                                f"[bold]{self.pairing_round[i][1]['last_name']} prennent 0.5 point[/bold]"
                            )
                            self.pairing_round[i][0]["score"] += 0.5
                            self.pairing_round[i][1]["score"] += 0.5
                        break
                # le score doit être mis sur un match
                # Un match, c'est un truple de liste de 2 joueurs et 2 scores
                # en fin de match stocker tous les rounds dans TOUR
                # ex: Tour(match1, match2, match3...)
                # from tuple to list to allow editing

                self.pairing_round = tuple(self.pairing_round)
                # self.player_controller.update_score(self.pairing_round)
                # self.pairing_round = TournamentController(self.tournament_data()).set_pairing_next_round(
                #    self.players_choice
                # )
                self.console.print(f"\n\n[bold]Match {i} Terminé[/bold]\n")
