"""Display all players registred and allow to change ranks."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from controllers.player_controller import PlayerController
from models.tables import Player

from .screen_and_sys_func import clear_screen
from .validation import display_error


class DisplayPlayers:
    def __init__(self):
        self.console = Console()
        self.player_model = Player()
        self.player_controller = PlayerController()

    def display_all_players(self, sort_option=""):
        clear_screen(0)
        self.console.print(
            "[bold][italic yellow]VOS JOUEURS[/italic yellow][/bold]\n",
            style=None,
            justify="center",
        )
        if not sort_option:
            player_list = self.player_controller.display_all_registred_players()
        elif sort_option in ["ranking", "last_name"]:
            if sort_option == "ranking":
                player_list = self.player_controller.sort_player_by_ranking()
            else:
                player_list = self.player_controller.sort_player_by_lastname()

        player_table = Table(title="")
        player_table.add_column("id", justify="center", style="white", no_wrap=True)
        player_table.add_column("identité", justify="center", style="white", no_wrap=True)
        player_table.add_column("date naissance", justify="center", style="white", no_wrap=True)
        player_table.add_column("genre", justify="center", style="white", no_wrap=True)
        player_table.add_column("rank", justify="center", style="white", no_wrap=True)
        for player in player_list:
            player_table.add_row(
                f"{player['id']}",
                f"{player['last_name']} {player['first_name']}",
                f"{player['date_of_birth']}",
                f"{player['gender']}",
                f"{player['ranking']}",
            )
        self.console.print(player_table)
        self.console.print(
            Panel.fit(
                "[bold green]Menu:[/bold green]\n\n"
                "[bold green]1)[/bold green] [bold]Selectionner un joueur[/bold]\n"
                "[bold green]2)[/bold green] [bold]Afficher par ordre alphabetique[/bold]\n"
                "[bold green]3)[/bold green] [bold]Afficher par rang[/bold]\n"
                "[bold green]4)[/bold green] [bold]Retour au menu principal[/bold]\n",
                border_style="red",
            )
        )
        self.display_player_menu_choice()

    def display_player_menu_choice(self):
        player_select_choice = input("Choisir: ")
        if player_select_choice == "1":
            self.display_player_id_select()
        elif player_select_choice == "2":
            self.display_all_players("last_name")
            self.display_player_menu_choice()
        elif player_select_choice == "3":
            self.display_all_players("ranking")
            self.display_player_menu_choice()
        elif player_select_choice == "4":
            return
        else:
            self.console.print(display_error("wrong_input_player_display_choice"))
            self.display_player_menu_choice()

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
        player_table = Table(title="")
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
                    return self.display_all_players()
                else:
                    self.console.print(display_error("wrong_turn_type_entry"))
                    return self.display_asking_player_rank_change(name, id)
            elif response.lower() == "n":
                self.console.print("\n[bold]Edition annulée...[/bold]")
                clear_screen(1)
                self.display_all_players()
