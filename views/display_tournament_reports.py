"""import"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from controllers.tournament_controller import (PlayerController,
                                               TournamentController)
from models.tables import Player, Round, Tournament

from .screen_and_sys_func import clear_screen
from .validation import display_error


class TournamentReports:
    def __init__(self):
        self.console = Console()
        self.tournament_list = TournamentController().get_all_tournaments()
        self.tournament_data = []
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()
        self.tournament_model = Tournament()
        self.player_model = Player()

    def display_reports(self):
        clear_screen(0)
        self.console.print(
            "[bold][italic yellow]VOS RAPPORTS DE TOURNOIS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )

        tournament_table = Table(title="")
        tournament_table.add_column("id", justify="center", style="green", no_wrap=True)
        tournament_table.add_column("nom", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("lieu", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("date début", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("date fin", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("terminé?", justify="center", style="green", no_wrap=True)
        for tournament in self.tournament_list:
            done = "Oui" if int(tournament["number_of_round"]) == len(tournament["rounds"]) else "Non"
            tournament_table.add_row(
                f"{tournament['id']}",
                f"{tournament['tournament_name']}",
                f"{tournament['location']}",
                f"{tournament['tournament_date_begin']}",
                f"{tournament['tournament_date_end']}",
                f"{done}",
            )
        self.console.print(tournament_table)
        self.display_tournament_id_select()

    def display_tournament_id_select(self):
        tournament_selected_id = input("\nVeuillez selectionner l'identifiant (id) du tournoi: ")
        if tournament_selected_id != "":
            if not (tournament_selected_id.isdigit() and int(tournament_selected_id) > 0):
                self.console.print(display_error("main_choice_type"))
                return self.display_tournament_id_select()
            else:
                return self.display_tournament_data(int(tournament_selected_id))
        else:
            self.console.print(display_error("empty_field"))
            return self.display_tournament_id_select()

    def display_player_id_select(self):
        player_selected_id = input("\nVeuillez selectionner l'identifiant (id) du joueur: ")
        if player_selected_id != "":
            if not (player_selected_id.isdigit() and int(player_selected_id) > 0):
                self.console.print(display_error("main_choice_type"))
                return self.display_player_id_select()
            else:
                return self.display_player_data(int(player_selected_id))
        else:
            self.console.print(display_error("empty_field"))
            return self.display_player_id_select()

    def display_player_data(self, id):
        player = self.player_model.get_player_by_id(id)
        player_table = Table(title="[bold]Liste des participants[/bold]")
        player_table.add_column("id", justify="center", style="white", no_wrap=True)
        player_table.add_column("identitée", justify="center", style="white", no_wrap=True)
        player_table.add_column("date naissance", justify="center", style="white", no_wrap=True)
        player_table.add_column("genre", justify="center", style="white", no_wrap=True)
        player_table.add_column("rang", justify="center", style="green", no_wrap=True)
        player_table.add_row(
            f"{player['id']}",
            f"{player['last_name']} {player['first_name']}",
            f"{player['date_of_birth']}",
            f"{player['gender']}",
            f"[bold]{player['ranking']}[/bold]",
        )
        self.console.print(player_table)
        name = f"{player['first_name']} {player['last_name']}"
        self.display_asking_player_rank_change(name, id)

    def display_asking_player_rank_change(self, name, id):
        response = input(f"Changer le rang de {name}? (o/n): ")
        if not response.lower() in ["o", "n"]:
            self.console.print(display_error("wrong_input_choice_to_confirm"))
            return self.display_asking_player_rank_change(name, id)
        else:
            if response.lower() == "o":
                clear_screen(0)
                new_rank = input("Choisir un nouveau rang: ")
                if new_rank.isdigit() and int(new_rank) > 0:
                    # get player data and create new Player instance
                    edit_player = self.player_model.unset_data(self.player_model.get_player_by_id(id))
                    # change data in .ranking attribute
                    edit_player.ranking = new_rank
                    # update on table
                    edit_player.update(edit_player)
                    self.console.print(
                        f"\n[bold green]{name} est maintenant de rang {new_rank}\n[/bold green]"
                        "\n[bold green]Retour à la selection des joueurs...[/bold green]"
                    )
                    clear_screen(1)
                    return self.display_player_in_tournament()
                else:
                    self.console.print(display_error("wrong_turn_type_entry"))
                    return self.display_asking_player_rank_change(name, id)
            elif response.lower() == "n":
                self.console.print("\n[bold]Edition annulée...[/bold]")
                clear_screen(1)
                return self.display_player_in_tournament()

    def report_action_choice(self):
        action_choice = input("Choisir: ")
        if action_choice == "1":
            return self.display_player_in_tournament()
        elif action_choice == "2":
            return self.display_tournament_results()
        elif action_choice == "3":
            return
        else:
            self.console.print(display_error("wrong_input_report_display_choice"))
            return self.report_action_choice()

    def display_tournament_results_menu_choice(self):
        action_choice = input("Choisir: ")
        if action_choice == "1":
            return self.display_player_id_select()
        elif action_choice == "2":
            return self.display_reports()
        else:
            self.console.print(display_error("wrong_input_report_display_choice"))
            return self.report_action_choice()

    def display_tournament_results(self):
        clear_screen(0)
        self.console.print(
            "[bold][italic yellow]AFFICHE DES RESULTATS DE [/italic yellow][/bold]"
            f"[bold][italic yellow]'{self.tournament_data.tournament_name.upper()}'[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        round_data = Round().get_round_by_id(self.tournament_data.rounds)
        for round in round_data:
            round_table = Table(
                title=f"\n[bold cyan]{round['name']}\nDebut le[/bold cyan] "
                f"{round['time_begin']} | "
                f"[bold cyan]Fin le[/bold cyan] {round['time_end']}"
            )
            round_table.add_column("ID 1", justify="center", style="yellow", no_wrap=True)
            round_table.add_column("Compétiteur 1", justify="center", style="white", no_wrap=True)
            round_table.add_column("Score compétiteur 1", justify="center", style="green", no_wrap=True)
            round_table.add_column("ID 2", justify="center", style="yellow", no_wrap=True)
            round_table.add_column("Compétiteur 2", justify="center", style="white", no_wrap=True)
            round_table.add_column("Score compétiteur 2", justify="center", style="green", no_wrap=True)
            for match in round["list_of_completed_matchs"]:
                round_table.add_row(
                    f"{match[0][0]}",
                    f"{self.player_model.get_player_name_by_id(match[0][0])}",
                    f"[bold]{match[0][1]}[/bold]",
                    f"{match[1][0]}",
                    f"{self.player_model.get_player_name_by_id(match[1][0])}",
                    f"[bold]{match[1][1]}[/bold]",
                )
            self.console.print(round_table)
        self.console.print(
            Panel.fit(
                "[bold green]Menu:[/bold green]\n"
                "[bold green]1)[/bold green] [bold]Selectionner un joueur[/bold]\n"
                "[bold green]2)[/bold green] [bold]Retour[/bold]\n",
                border_style="red",
            )
        )
        self.display_tournament_results_menu_choice()

    def display_tournament_data(self, id):
        clear_screen(0)
        self.console.print(
            "[bold][italic yellow]RAPPORT DU TOURNOI[/italic yellow][/bold]",
            style=None,
            justify="center",
        )
        self.tournament_data = self.tournament_model.unset_data(self.tournament_controller.get_tournament_by_id(id))
        tournament_table = Table(title="")
        tournament_table.add_column("id", justify="center", style="green", no_wrap=True)
        tournament_table.add_column("nom", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("lieu", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("date début", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("date fin", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("Nbr. Round", justify="center", style="white", no_wrap=True)
        tournament_table.add_column("description", justify="center", style="white", no_wrap=True)
        tournament_table.add_row(
            f"[bold]{self.tournament_data.id}[/bold]",
            f"{self.tournament_data.tournament_name}",
            f"{self.tournament_data.location}",
            f"{self.tournament_data.tournament_date_begin}",
            f"{self.tournament_data.tournament_date_end}",
            f"{self.tournament_data.number_of_round}",
            f"{self.tournament_data.description}",
        )
        self.console.print(tournament_table)
        self.console.print(
            Panel.fit(
                "[bold green]Menu:[/bold green]\n\n"
                "[bold green]1)[/bold green] [bold]Afficher compétiteurs[/bold]\n"
                "[bold green]2)[/bold green] [bold]Afficher les rounds et matchs[/bold]\n"
                "[bold green]3)[/bold green] [bold]Retour au menu principal[/bold]\n",
                border_style="red",
            )
        )

        self.report_action_choice()

    def display_player_in_tournament(self, sort_option=""):
        clear_screen(0)
        self.console.print(
            "[bold][italic yellow]VOS JOUEURS DANS LE TOURNOI [/italic yellow][/bold]"
            f"[bold][italic yellow]'{self.tournament_data.tournament_name.upper()}'[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        player_list = self.player_controller.display_all_player_in_tournament(self.tournament_data.players_choice)
        get_last_round_results = Round().get_round_by_id(self.tournament_data.rounds)[-1]["list_of_completed_matchs"]
        player_list = self.player_controller.add_temp_score_to_player_list(player_list, get_last_round_results)
        if sort_option in ["ranking", "last_name"]:
            if sort_option == "ranking":
                player_list = self.player_controller.sort_player_list(player_list, "ranking")
            else:
                player_list = self.player_controller.sort_player_list(player_list, "last_name")

        player_table = Table(title="")
        player_table.add_column("id", justify="center", style="white", no_wrap=True)
        player_table.add_column("identitée", justify="center", style="white", no_wrap=True)
        player_table.add_column("date naissance", justify="center", style="white", no_wrap=True)
        player_table.add_column("genre", justify="center", style="white", no_wrap=True)
        player_table.add_column("rang", justify="center", style="white", no_wrap=True)
        player_table.add_column("score compétition", justify="center", style="cyan", no_wrap=True)
        for player in player_list:
            player_table.add_row(
                f"[bold]{player.id}[/bold]",
                f"{player.last_name} {player.first_name}",
                f"{player.date_of_birth}",
                f"{player.gender}",
                f"{player.ranking}",
                f"[bold]{player.score}[/bold]",
            )
        self.console.print(player_table)
        self.console.print(
            Panel.fit(
                "[bold green]Menu:[/bold green]\n\n"
                "[bold green]1)[/bold green] [bold]Selectionner un joueur[/bold]\n"
                "[bold green]2)[/bold green] [bold]Afficher par ordre alphabetique[/bold]\n"
                "[bold green]3)[/bold green] [bold]Afficher par rang[/bold]\n"
                "[bold green]4)[/bold green] [bold]Retour aux rapports[/bold]",
                border_style="red",
            )
        )
        self.display_player_menu_choice()

    def display_player_menu_choice(self):
        player_select_choice = input("Choisir: ")
        if player_select_choice == "1":
            self.display_player_id_select()
        elif player_select_choice == "2":
            self.display_player_in_tournament("last_name")
        elif player_select_choice == "3":
            self.display_player_in_tournament("ranking")
            self.display_player_menu_choice()
        elif player_select_choice == "4":
            return self.display_reports()
        else:
            self.console.print(display_error("wrong_input_player_report_display_choice"))
            self.display_player_menu_choice()
