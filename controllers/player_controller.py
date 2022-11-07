"""import"""
from models.tables import Player
from tinydb import TinyDB, Query, where


class PlayerController:
    def __init__(self):
        self.player_model = Player()
        self.db = TinyDB("db_chess.json")

    def get_players_list(self):
        return Player().display_data()

    def update_score(self, id_list: list):
        # print(id_list)
        for player in id_list:
            self.db.table("players").update_multiple(
                [
                    ({"score": player[0]["score"]}, where("last_name") == player[0]["last_name"]),
                    ({"score": player[1]["score"]}, where("last_name") == player[1]["last_name"]),
                ]
            )

    def save(self, player_data):
        self.player_model.save(player_data)

    def get_players_by_parameters(self, id_list: list, parameter: str):
        # sort list by ranking or score
        players_data = sorted(self.db.table("players").all(), key=lambda d: d[parameter], reverse=True)
        # return dict from previous list
        return {
            i: {
                "first_name": players_data[i]["first_name"],
                "last_name": players_data[i]["last_name"],
                "ranking": players_data[i]["ranking"],
                "score": players_data[i]["score"],
            }
            for i in range(0, len(players_data))
            if players_data[i].doc_id in id_list
        }


print(Player().display_data())
