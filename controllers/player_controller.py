"""import"""
from models.tables import TimeController, Player
from tinydb import TinyDB, Query, where


class PlayerController:
    def __init__(self):
        self.time_controller = TimeController
        self.player_controller = Player()
        self.db = TinyDB("db_chess.json")

    def get_players_list(self):
        return self.player_controller.display_data()
    
    def update_score(self, id_list: list):
        #print(id_list)
        for i in range(0, len(id_list)):
            self.db.table("players").update_multiple([
                ({'score': id_list[i][0]["score"]}, where('id') == id_list[i][0]["id"]),
                ({'score': id_list[i][1]["score"]}, where('id') == id_list[i][1]["id"]),
            ])

    def save_player(self, data: dict):
        new_player = Player(data)
        return new_player.save()

    def get_players_by_parameters(self, id_list: list, parameter:str):
        # sort list by ranking
        players_data = sorted(self.db.table("players").all(), key=lambda d: d[parameter], reverse=True)
        # return dict from previous list
        return {
            i: {
                "id": players_data[i]["id"],
                "last_name": players_data[i]["last_name"],
                "first_name": players_data[i]["first_name"],
                "ranking": players_data[i]["ranking"],
                "score": players_data[i]["score"]
            }
            for i in range(0, len(players_data))
            if players_data[i]["id"] in id_list
        }

    