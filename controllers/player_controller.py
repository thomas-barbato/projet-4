"""import"""
from models.tables import Player, Tour
from tinydb import TinyDB, Query, where
from operator import itemgetter
from operator import attrgetter


class PlayerController:
    def __init__(self):
        self.player_model = Player()
        self.db = TinyDB("db_chess.json")

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

    def sort_players_by_rank(self, id_list):
        players_data = sorted(self.db.table("players").all(), key=lambda d: d["ranking"], reverse=True)
        results = [
            {
                "first_name": players_data[i]["first_name"],
                "last_name": players_data[i]["last_name"],
                "date_of_birth": players_data[i]["date_of_birth"],
                "gender": players_data[i]["gender"],
                "ranking": players_data[i]["ranking"],
                "score": players_data[i]["score"],
                "id": players_data[i]["id"],
            }
            for i in range(0, len(players_data))
            if players_data[i]["id"] in id_list
        ]
        players_in_tournament = {}
        players_in_tournament[0] = results[0]
        players_in_tournament[1] = results[1]
        players_in_tournament[2] = results[2]
        players_in_tournament[3] = results[3]
        players_in_tournament[4] = results[4]
        players_in_tournament[5] = results[5]
        players_in_tournament[6] = results[6]
        players_in_tournament[7] = results[7]

        return self._set_teams(players_in_tournament)

    def _set_teams(self, player_list):
        first_team: dict = []
        second_team: dict = []
        for i in range(0, len(player_list.keys())):
            if i % 2 == 0:
                first_team.append(
                    {
                        "first_name": player_list[i]["first_name"],
                        "last_name": player_list[i]["last_name"],
                        "date_of_birth": player_list[i]["date_of_birth"],
                        "gender": player_list[i]["gender"],
                        "ranking": player_list[i]["ranking"],
                        "score": player_list[i]["score"],
                        "id": player_list[i]["id"],
                    }
                )
            else:
                second_team.append(
                    {
                        "first_name": player_list[i]["first_name"],
                        "last_name": player_list[i]["last_name"],
                        "date_of_birth": player_list[i]["date_of_birth"],
                        "gender": player_list[i]["gender"],
                        "ranking": player_list[i]["ranking"],
                        "score": player_list[i]["score"],
                        "id": player_list[i]["id"],
                    }
                )
        return tuple(zip(first_team, second_team))

    def sort_players_by_score(self, tour_instance):
        tour_instance_id_list = tour_instance
        player_objects_list = []
        temp_player_list = []
        first_team: dict = []
        second_team: dict = []
        
        tournament_players_1_data = [
            [tour_instance_id_list[i][0][0], tour_instance_id_list[i][0][1]] for i in range(len(tour_instance_id_list))
        ]
        
        tournament_players_2_data = [
            (tour_instance_id_list[i][1][0], tour_instance_id_list[i][1][1]) for i in range(len(tour_instance_id_list))
        ]
        
        player_concat_list = tournament_players_1_data + tournament_players_2_data
        in_db = Query()
        # 0 = id ; 1 = score
        for i in range(len(player_concat_list)):
            player_search = self.db.table('players').search(in_db.id == player_concat_list[i][0])[0]
            # store instance with data in list
            player_objects_list.append(Player().unset_data(player_search))
            # get instance
            player_content = player_objects_list[i]
            # allow edition
            edit_data = player_content.set_data()
            # change score
            edit_data["score"] = player_concat_list[i][1]
            # save score in instance
            player_objects_list[i] = player_content.unset_data(edit_data)
        
        # Sorts players by score or by ranking if they are equals
        player_objects_list.sort(key=attrgetter("score", 'ranking'), reverse=True)
        for i in range(len(player_objects_list)):
            player_data = player_objects_list[i]
            player_get_data = player_data.set_data()
            if i % 2 == 0:
                first_team.append(
                    {
                        "first_name": player_get_data["first_name"],
                        "last_name": player_get_data["last_name"],
                        "date_of_birth": player_get_data["date_of_birth"],
                        "gender": player_get_data["gender"],
                        "ranking": player_get_data["ranking"],
                        "score": player_get_data["score"],
                        "id": player_get_data["id"],
                    }
                )
            else:
                second_team.append(
                    {
                        "first_name": player_get_data["first_name"],
                        "last_name": player_get_data["last_name"],
                        "date_of_birth": player_get_data["date_of_birth"],
                        "gender": player_get_data["gender"],
                        "ranking": player_get_data["ranking"],
                        "score": player_get_data["score"],
                        "id": player_get_data["id"],
                    }
                )
        return tuple(zip(first_team, second_team))
        

    def get_players_by_parameters(self, id_list: list, parameter: str):
        # sort list by ranking or score
        players_data = sorted(self.db.table("players").all(), key=lambda d: d[parameter], reverse=True)
        # return dict from previous list
        return [
            {
                "first_name": players_data[i]["first_name"],
                "last_name": players_data[i]["last_name"],
                "ranking": players_data[i]["ranking"],
                "score": players_data[i]["score"],
                "id": players_data[i]["id"],
            }
            for i in range(0, len(players_data))
            if players_data[i]["id"] in id_list
        ]
