"""import"""
from tinydb import TinyDB, Query
from models.tables import Tournament, Player, Round
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

    # need to format data to be able to add in in json.
    def save_current_round(self, tournament_object, round_object_list):
        round_list = []
        tournament_data = tournament_object
        for round in round_object_list[0].list_of_completed_matchs:
            player_1 = round[0][0]
            player_2 = round[1][0]
            round_list.append([[player_1.id, round[0][1]], [player_2.id, round[1][1]]])

        Round(round_object_list[0].time_begin, round_object_list[0].time_end, round_list).save()
        round_id = Round(round_object_list[0].time_begin, round_object_list[0].time_end, round_list).get_round_id()
        tournament_data["rounds"].append(round_id)
        update_tournament = Tournament().unset_data(tournament_data)
        update_tournament.update(tournament_data)
        round_list.clear()
