"""import"""
import os
import sys
from tinydb import TinyDB, Query, where

if os.path.basename(__file__) != "main.py":
    PROJECT_CWD = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1])
    DIR = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1]) + os.sep + "db_chess.json"
    sys.path.append(PROJECT_CWD)
    sys.path.append(os.path.join(PROJECT_CWD, "models"))
    sys.path.append(os.path.join(PROJECT_CWD, "views"))
else:
    DIR = f"{os.sep}".join(os.getcwd().split(os.sep)) + os.sep + "db_chess.json"


from models.tables import TimeController, Player, Tournament


class Controller:
    def __init__(self):
        self.db = TinyDB(DIR)
        self.time_controller = TimeController
        self.player_controller = Player()
        self.tournament_controller = Tournament()

    def check_enum_status(self, input: str):
        if input in self.time_controller._value2member_map_:
            return True

    def get_players_list(self):
        return self.player_controller.display_data()

    def get_tournament_list(self):
        return self.tournament_controller.display_data()

    def save_tournament(self, data: dict):
        new_tournament = Tournament(data)
        return new_tournament.save()

    def save_player(self, data: dict):
        new_player = Player(data)
        return new_player.save()

    def _get_players_by_id(self, id_list: list):
        in_db = Query()
        # sort list by ranking
        players_data = sorted(self.db.table("players").all(), key=lambda d: d["ranking"], reverse=True)
        # return dict from previous list
        return {
            i: {
                "id": players_data[i]["id"],
                "first_name": players_data[i]["first_name"],
                "last_name": players_data[i]["last_name"],
                "ranking": players_data[i]["ranking"],
            }
            for i in range(0, len(players_data))
            if players_data[i]["id"] in id_list
        }

    def _set_teams(self, player_id_list: list):
        player_list = self._get_players_by_id(player_id_list)
        first_team: dict = []
        second_team: dict = []
        for i in range(0, len(player_list.keys())):
            if i % 2 == 0:
                first_team.append(
                    {
                        "id": player_list[i]["id"],
                        "last_name": player_list[i]["last_name"],
                        "first_name": player_list[i]["first_name"],
                        "ranking": player_list[i]["ranking"],
                    }
                )
            else:
                second_team.append(
                    {
                        "id": player_list[i]["id"],
                        "last_name": player_list[i]["last_name"],
                        "first_name": player_list[i]["first_name"],
                        "ranking": player_list[i]["ranking"],
                    }
                )
        return first_team, second_team

    def set_pairing(self, player_id_list: list):
        first_team, second_team = self._set_teams(player_id_list)
        pairing = list(zip(first_team, second_team))
        for i in range(0, len(pairing)):
            print(pairing[i])


x = Controller().set_pairing([0,1,2,3,4,5,6,7])