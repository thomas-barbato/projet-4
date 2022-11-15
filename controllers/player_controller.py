"""import"""
from models.tables import Player, Round
from tinydb import TinyDB, where
from operator import attrgetter


class PlayerController:
    def __init__(self):
        self.player_model = Player()
        self.db = TinyDB("db_chess.json")

    def update_score(self, id_list: list):
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
        first_team: list = []
        second_team: list = []
        for i in range(0, len(player_list.keys())):
            if i % 2 == 0:
                first_team.append(
                    [
                        Player(
                            player_list[i]["first_name"],
                            player_list[i]["last_name"],
                            player_list[i]["date_of_birth"],
                            player_list[i]["gender"],
                            player_list[i]["ranking"],
                            player_list[i]["score"],
                            player_list[i]["id"],
                        ),
                        player_list[i]["score"],
                    ]
                )
            else:
                second_team.append(
                    [
                        Player(
                            player_list[i]["first_name"],
                            player_list[i]["last_name"],
                            player_list[i]["date_of_birth"],
                            player_list[i]["gender"],
                            player_list[i]["ranking"],
                            player_list[i]["score"],
                            player_list[i]["id"],
                        ),
                        player_list[i]["score"],
                    ]
                )
        return tuple(zip(first_team, second_team))

    def sort_players_by_score(self, tournament_object):
        self.tournament_object = tournament_object
        self.round_model = Round()
        self.player_model = Player()
        self.player_objects_list = []
        self.matchs_played = []
        first_team: dict = []
        second_team: dict = []
        self.round_data = self.round_model.get_last_round_by_id(self.tournament_object.rounds)

        for player in self.round_data[0]["list_of_completed_matchs"]:
            player_1_id = player[0][0]
            player_1_score = player[0][1]
            player_1_data = self.player_model.get_player_by_id(player_1_id)
            player_2_id = player[1][0]
            player_2_score = player[1][1]
            player_2_data = self.player_model.get_player_by_id(player_2_id)
            # create new player list
            self.player_objects_list.append(
                Player(
                    player_1_data["first_name"],
                    player_1_data["last_name"],
                    player_1_data["date_of_birth"],
                    player_1_data["gender"],
                    player_1_data["ranking"],
                    player_1_score,
                    player_1_data["id"],
                )
            )
            self.player_objects_list.append(
                Player(
                    player_2_data["first_name"],
                    player_2_data["last_name"],
                    player_2_data["date_of_birth"],
                    player_2_data["gender"],
                    player_2_data["ranking"],
                    player_2_score,
                    player_2_data["id"],
                )
            )
            # set match played list
            self.matchs_played.append([player_1_data["id"], player_2_data["id"]])
        # sort team by score, if score is equal
        # then by ranking
        # reversed
        self.player_objects_list.sort(key=attrgetter("score", "ranking"), reverse=True)
        self.round_instance = Round()
        # if player 1 and player 2 already played together:
        # then change player 2 to player 3.
        if [self.player_objects_list[0].id, self.player_objects_list[1].id] in self.matchs_played:
            temp_player_place = self.player_objects_list[1]
            self.player_objects_list[1] = self.player_objects_list[2]
            self.player_objects_list[2] = temp_player_place

        for i in range(len(self.player_objects_list)):
            player_data = self.player_objects_list[i]
            player_get_data = player_data.set_data()
            if i % 2 == 0:
                first_team.append([self.player_objects_list[i], player_get_data["score"]])
            else:
                second_team.append([self.player_objects_list[i], player_get_data["score"]])
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
