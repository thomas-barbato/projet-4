"""import"""
import os
import sys
from tinydb import TinyDB, Query
from models.tables import Tournament, Player
from controllers.player_controller import PlayerController


class TournamentController:
    def __init__(self, tournament_data={}):
        self.db = TinyDB("db_chess.json")
        self.tournament_data = tournament_data
        self.tournament_model = Tournament(self.tournament_data)
        self.player_in_tournament = []
        self.player_model_instance = Player()
        self.playerController = PlayerController()
        self.pairing: tuple() = ()
        self.matchs = []

    def save(self, tournament_data):
        self.tournament_model.save(tournament_data)

    def get_tournament_list(self):
        return self.tournament_model.display_data()
    
    def get_player_list(self):
        return self.player_model_instance.display_data() 

    def set_player_instance(self):
        pass

    def _set_teams(self, player_id_list: list, parameter):
        players_list = sorted(self.player_model.display_data(), key=lambda d: d[parameter], reverse=True)
        player_list = self.playerController.get_players_by_parameters(player_id_list, parameter)
        first_team: dict = []
        second_team: dict = []
        for i in range(0, len(player_list.keys())):
            if i % 2 == 0:
                first_team.append(
                    {
                        "last_name": player_list[i]["last_name"],
                        "ranking": player_list[i]["ranking"],
                        "score": player_list[i]["score"],
                    }
                )
            else:
                second_team.append(
                    {
                        "last_name": player_list[i]["last_name"],
                        "ranking": player_list[i]["ranking"],
                        "score": player_list[i]["score"],
                    }
                )
        return first_team, second_team

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
