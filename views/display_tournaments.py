"""def display_create_tournament_view(self):
    controller_data = TournamentController()
    self.console.print(
        "[bold][italic yellow]CONSULTER LES TOURNOIS CRÉÉS[/italic yellow][/bold]\n",
        style=None,
        justify="center",
    )
    if len(controller_data.get_tournament_list()) >= 1:
        table = Table(title="")
        table.add_column("id", justify="center", style="green", no_wrap=False)
        table.add_column("nom", justify="center", style="cyan", no_wrap=False)
        table.add_column("lieu", justify="center", style="cyan", no_wrap=False)
        table.add_column("date_debut", justify="center", style="cyan", no_wrap=False)
        table.add_column("date_fin", justify="center", style="cyan", no_wrap=False)
        table.add_column("nbr_tour", justify="center", style="cyan", no_wrap=False)
        table.add_column("nbr_manche", justify="center", style="cyan", no_wrap=False)
        table.add_column("time", justify="center", style="cyan", no_wrap=False)
        table.add_column("joueurs", justify="center", style="cyan", no_wrap=False)
        table.add_column("description", justify="center", style="cyan", no_wrap=False)

        for tournament in controller_data.get_tournament_list():
            table.add_row(
                str(tournament["id"]),
                str(tournament["name"]),
                str(tournament["location"]),
                str(tournament["tournament_date_begin"]),
                str(tournament["tournament_date_end"]),
                str(tournament["number_of_turn"]),
                str(tournament["number_of_round"]),
                str(tournament["time_controller_choice"]),
                str(tournament["players_list"]),
                str(tournament["description"]),
            )

        self.console.print(table)
        self.console.print(
            "[italic]\n\nAppuyez sur [/italic]"
            "[bold green]'o'[/bold green][italic] pour revenir au menu ou [/italic]"
            "[bold green]'q'[/bold green][italic]"
            " pour quitter[/italic]\n\n"
        )
        while True:
            response = input("Reponse (o / q): ")
            if response.lower() != "q" and response.lower() != "o":
                self.console.print(display_error("wrong_input_choice_to_save"))
            elif response.lower() == "o":
                self.console.print("[bold]vous allez être redirigé vers le menu principal.[/bold]")
                clear_screen(1)
                return self.display_main_menu()
            elif response.lower() == "q":
                self.console.print("[bold]Le programme va maintenant se terminer, à très bientôt.\n[/bold]")
                clear_screen(1)
                return exit_to_console(0)
    else:
        self.console.print(display_error("no_tournament_created"))
        clear_screen(1)
        return self.display_create_menu()
"""