"""import"""
from .validation import display_error
from .screen_and_sys_func import clear_screen
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from .menu import TournamentMenu
from models.tables import Tournament, Match, Round
from rich.console import Console
from rich.table import Table


class Playmatch:
    def __init__(self, data):
        self.console = Console()
        self.pairing: tuple = ()
        self.player_controller: PlayerController = PlayerController()
        self.tournament_controller: TournamentController = TournamentController()
        self.match_model: Match = Match()
        self.round_model: Round = Round()
        self.time_begin: str = ""
        self.time_end: str = ""
        self.name: str = f"Round {self.round_model.NUMBER_OF_TOUR}"
        self.list_of_completed_match: list = []
        self.matchs_list_per_tour: list = []
        self.current_rounds: list = []
        # set data in Tournament instance
        self.tournament_object: Tournament = Tournament().unset_data(data)
        # allow editing.
        self.tournament_object_editable_data: Tournament = self.tournament_object.set_data()

    def display_title(self):
        self.console.print(
            "[bold][italic yellow]LE TOURNOI[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )

    def set_pairing(self):
        self.matchs_list_per_tour.clear()
        self.list_of_completed_match.clear()
        if len(self.tournament_object.rounds) == 0:
            self.pairing = self.player_controller.sort_players_by_rank(self.tournament_object.players_choice)
        else:
            self.pairing = self.player_controller.sort_players_by_score(self.tournament_object)
        for pairing in self.pairing:
            self.matchs_list_per_tour.append(Match(pairing[0][0], pairing[1][0], pairing[0][1], pairing[1][1]))

    def display_pairing(self):
        pairing_table = Table(title=f"\n\n[bold]Paires round {self.round_model.NUMBER_OF_TOUR}[/bold]\n")
        pairing_table.add_column("Numéro Equipe", justify="center", style="white", no_wrap=True)
        pairing_table.add_column("Competiteur 1", justify="center", style="white", no_wrap=True)
        pairing_table.add_column("Competiteur 2", justify="center", style="white", no_wrap=True)
        for i in range(0, len(self.pairing)):
            pairing_table.add_row(
                f"{i}",
                f"{self.pairing[i][0][0].first_name} {self.pairing[i][0][0].last_name}",
                f"{self.pairing[i][1][0].first_name} {self.pairing[i][1][0].last_name}",
            )
        self.console.print(pairing_table)

    def display_rules(self, round_count):
        if self.round_model.NUMBER_OF_TOUR == 1:
            self.console.print(
                f"\n[bold]Le tournoi va se dérouler en {self.tournament_object.number_of_round} tours.[/bold]\n"
                "[bold]Attribution des scores:[/bold]\n"
                "un match gagné = 1 point\n"
                "un match perdu = 0 point\n"
                "un match nul = 0.5 pour les deux participants.\n"
            )
        else:
            self.console.print(
                f"\n[bold]{self.tournament_object.number_of_round-round_count} tours restants.[/bold]\n"
                "[bold]Attribution des scores:[/bold]\n"
                "un match gagné = 1 point\n"
                "un match perdu = 0 point\n"
                "un match nul = 0.5 pour les deux participants.\n"
            )

    def display_end_tournament(self):

        self.console.print("\n\n[bold]Le tournoi est maintenant terminé[/bold]\n")
        response: str = input("Voulez-vous afficher les résultats ? (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_continue"))
            self.display_end_tournament()
        elif response.lower() == "o":
            pass
            # DisplayTournaments().display_selected_tournaments(self.tournament_object)
        elif response.lower() == "n":
            clear_screen(0)
            self.console.print("\n\n[bold]Vous allez être redirigé vers la page d'accueil.[/bold]\n")
            return TournamentMenu().display_menu_choices()

    def start_chronometer(self):
        response: str = input("Lancer le chronomètre ? (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_continue"))
            self.start_chronometer()
        elif response.lower() == "o":
            self.time_begin = self.round_model.get_time_now()
        elif response.lower() == "n":
            self.start_chronometer()

    def end_chronometer(self):
        response: str = input("Arrêter le chronomètre ? (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_continue"))
            self.end_chronometer()
        elif response.lower() == "o":
            self.time_end = self.round_model.get_time_now()
        elif response.lower() == "n":
            self.end_chronometer()

    def select_result(self):
        response: str = input("Résultat: ")
        if response not in ["1", "2", "3"]:
            self.console.print(display_error("wrong_match_result_input"))
            return self.select_result()
        else:
            return response

    def save_tournament_current_tour_and_exit(self):
        round_name = f"Round {self.round_model.NUMBER_OF_TOUR}"
        self.current_rounds.append(Round(round_name, self.time_begin, self.time_end, self.list_of_completed_match))
        self.tournament_controller.save_current_round(self.tournament_object, self.current_rounds)
        self.current_rounds.clear()
        response: str = input("Voulez-vous sauvegarder et quitter la manche en cours ? (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_continue"))
        elif response.lower() == "o":
            clear_screen(1)
            self.console.print("[bold]Sauvegarde terminée...[/bold]")
            self.console.print("\n[bold]vous allez être redirigé vers le menu principal.[/bold]")
            return TournamentMenu().display_menu_choices()

    def display_tournament_result(self):
        pass

    def display_tournament_begin(self):
        clear_screen(0)
        self.display_title()
        self.round_model.NUMBER_OF_TOUR = (
            len(self.tournament_object.rounds) + 1 if len(self.tournament_object.rounds) > 0 else 1
        )
        round_count = len(self.tournament_object.rounds) if len(self.tournament_object.rounds) > 0 else 1

        for i in range(len(self.tournament_object.rounds), int(self.tournament_object.number_of_round)):
            # clean pairing
            self.pairing = ()
            self.set_pairing()
            self.display_pairing()
            self.display_rules(round_count)
            self.start_chronometer()
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
                        match.player_1.score += float(1.0)
                        match.player_2.score += float(0)
                    elif choice == "2":
                        self.console.print(
                            f"\n[bold]Le competiteur [/bold]"
                            f"[bold]{match.player_2['last_name']} prend 1 point[/bold]"
                        )
                        match.player_1.score += float(0.0)
                        match.player_2.score += float(1.0)
                    elif choice == "3":
                        self.console.print(
                            f"\n[bold]Les competiteurs {match.player_1['last_name']}[/bold]"
                            "[bold] et [/bold]"
                            f"[bold]{match.player_2['last_name']} prennent 0.5 point[/bold]"
                        )
                        match.player_1.score += float(0.5)
                        match.player_2.score += float(0.5)
                    # Un match unique doit être stocké sous la forme d'un tuple
                    # contenant deux listes, chacune contenant deux éléments :
                    # une référence à une instance de joueur et un score.
                    self.list_of_completed_match.append(
                        tuple(
                            [
                                [match.player_1, match.player_1.score],
                                [match.player_2, match.player_2.score],
                            ]
                        )
                    )
                    break
            # end clock
            self.end_chronometer()
            # save new turn
            self.save_tournament_current_tour_and_exit()
            # clean lists
            self.round_model.NUMBER_OF_TOUR += 1
        self.display_end_tournament()
