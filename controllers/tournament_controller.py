"""import"""
import os
import sys
from tinydb import TinyDB, Query
from models.tables import Tournament, Player, Tour
from controllers.player_controller import PlayerController


class TournamentController:
    def __init__(self, tournament_data=[]):
        self.db = TinyDB("db_chess.json")
        self.tournament_data = tournament_data
        self.tournament_model = Tournament(self.tournament_data)
        self.player_model_instance = Player()
        self.playerController = PlayerController()

    def save(self):
        self.tournament_model.save(self.tournament_data)

    def get_tournament_instance(self):
        return self.tournament_model

    def get_tournament_by_name(self, tournament_name):
        return self.tournament_model.get_tournament_by_name(tournament_name)

    def get_tournament_by_id(self, id):
        return self.tournament_model.get_tournament_by_id(id)

    def get_all_tournaments(self):
        return self.tournament_model.display_tournament_data()

    def check_if_tournament_id_exists(self, id):
        return self.tournament_model.check_id(id)

    def get_players_list(self):
        return self.db.table("players").all()

    def get_players_name_by_tournament_id(self, tournament_id):
        player_choices_list = self.db.table("tournaments").get(Query().id == tournament_id)["players_choice"]
        result = [
            {"first_name": r["first_name"], "last_name": r["last_name"]}
            for r in self.db.table("players")
            if r["id"] in player_choices_list
        ]
        format_result = ", ".join(
            [f"{result[i]['first_name']} {result[i]['last_name']}" for i in range(0, len(result))]
        )
        return format_result

    def set_pairing_first_round(self, player_id_list: list):
        first_team, second_team = self._set_teams(player_id_list, "ranking")
        self.pairing = tuple(zip(first_team, second_team))
        return self.pairing

    # change here , from player table to data sended list.
    # to be able to change score from tournament to another tournament
    def set_pairing_next_round(self, player_id_list: list):
        first_team, second_team = self._set_teams(player_id_list, "score")
        self.pairing = tuple(zip(first_team, second_team))
        return self.pairing

    def save_current_tour(self, tournament_object, tour_object):
        tour = tour_object.set_data()
        tour_data = {}
        tour_data["time_begin"] = tour["time_begin"]
        tour_data["time_end"] = tour["time_end"]
        tour_data["list_of_completed_matchs"] = tour["list_of_completed_matchs"]
        Tour().save(tour_data)
        tour_id = Tour().get_tour_id(tour_data)

        tournament_data = tournament_object.set_data()
        tournament_data["round_ids"].append(int(tour_id))
        update_tournament = Tournament().unset_data(tournament_data)
        update_tournament.update(tournament_data)

    def save_current_round(self, tournament_data):
        pass
