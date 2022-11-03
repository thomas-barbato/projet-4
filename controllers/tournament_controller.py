"""import"""
import os
import sys
from tinydb import TinyDB, Query

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from models.tables import TimeController, Tournament
from controllers.player_controller import PlayerController


class TournamentController:
    def __init__(self, tournament_data={}):
        self.time_controller = TimeController
        self.tournament_data = tournament_data
        self.tournament_controller = Tournament(self.tournament_data)
        self.playerController = PlayerController()
        self.db = TinyDB("db_chess_tournament.json")
        self.pairing: tuple() = ()
        self.matchs = []

    def save(self):
        self.tournament_controller.save()

    def update_pairing(self, tournament_data, tournament_name, players_choice):
        tournament_id = self.db.table("tournaments").search(
            (Query().name == tournament_name) & (Query().players_choice == players_choice)
        )[0]["id"]
        return self.db.table("tournaments").update({"pairing": tournament_data}, Query().id == tournament_id)

    def check_enum_status(self, input: str):
        if input in self.time_controller._value2member_map_:
            return True

    def get_tournament_list(self):
        return self.tournament_controller.display_data()

    def _set_first_teams(self, player_id_list: list, parameter):
        player_list = self.playerController.get_players_by_parameters(player_id_list, parameter)
        first_team: dict = []
        second_team: dict = []
        for i in range(0, len(player_list.keys())):
            if i % 2 == 0:
                first_team.append(
                    {
                        "id": player_list[i]["id"],
                        "last_name": player_list[i]["last_name"],
                        "ranking": player_list[i]["ranking"],
                        "score": player_list[i]["score"],
                    }
                )
            else:
                second_team.append(
                    {
                        "id": player_list[i]["id"],
                        "last_name": player_list[i]["last_name"],
                        "ranking": player_list[i]["ranking"],
                        "score": player_list[i]["score"],
                    }
                )
        return first_team, second_team

    def set_pairing_first_round(self, player_id_list: list):
        first_team, second_team = self._set_first_teams(player_id_list, "ranking")
        self.pairing = tuple(zip(first_team, second_team))
        return self.pairing

    def set_pairing_next_round(self, player_id_list: list):
        first_team, second_team = self._set_first_teams(player_id_list, "score")
        self.pairing = tuple(zip(first_team, second_team))
        print(self.pairing)
        return self.pairing

    def get_pairing(self):
        return self.pairing
    
    