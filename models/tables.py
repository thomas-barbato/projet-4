"""import"""
from tinydb import TinyDB, Query, where
from enum import Enum
from datetime import datetime
import pytz

db = TinyDB("db_chess.json")


class Table:
    def __init__(self, data: dict = {}, table_name: str = ""):
        self.table = ""

    def clear_table(self):
        db.table(self.table).truncate()

    def get_id_list(self):
        return [id.doc_id for id in db.table(self.table)]

    # allow to get class items.
    def __getitem__(self, key):
        return self.__dict__[key]


class Player(Table):
    def __init__(
        self, first_name=None, last_name=None, date_of_birth=None, gender=None, ranking=None, score=None, id=None
    ):
        self.table = "players"
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.date_of_birth: str = date_of_birth
        self.gender: str = gender
        self.ranking: int = ranking
        self.score: float = score
        self.id = id
        self.table = db.table(self.table)

    # allow editing.
    def set_data(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "ranking": self.ranking,
            "score": self.score,
            "id": self.id,
        }

    # allow to set data in instance
    def unset_data(self, data):
        first_name: str = data["first_name"]
        last_name: str = data["last_name"]
        date_of_birth: str = data["date_of_birth"]
        gender: str = data["gender"]
        ranking: int = data["ranking"]
        score: int = data["score"]
        id: int = data["id"]

        return Player(first_name, last_name, date_of_birth, gender, ranking, score, id)

    def save(self, player_data):
        new_player_id = self.table.insert(
            {
                "first_name": player_data[0],
                "last_name": player_data[1],
                "date_of_birth": player_data[2],
                "gender": player_data[3],
                "ranking": player_data[4],
                "score": player_data[5],
                "id": player_data[6],
            }
        )
        self.table.update({"id": new_player_id}, doc_ids=[new_player_id])

    def __str__(self):
        return f"{self.first_name} {self.last_name} est classé {self.ranking}\
            avec score de {self.score}"


class Tournament(Table):
    def __init__(
        self,
        tournament_name=None,
        location=None,
        tournament_date_begin=None,
        tournament_date_end=None,
        number_of_round=4,
        players_choice=None,
        time_controller_choice=None,
        description=None,
        round_ids=None,
        id=None,
    ):
        self.table = "tournaments"
        self.tournament_name: str = tournament_name
        self.location: str = location
        self.tournament_date_begin: str = tournament_date_begin
        self.tournament_date_end: str = tournament_date_end
        self.number_of_round: int = number_of_round
        self.players_choice: list = players_choice
        self.time_controller_choice: str = time_controller_choice
        self.description: str = description
        self.round_ids: list = round_ids
        self.id: int = id
        self.table = db.table(self.table)

    # allow editing.
    def set_data(self):
        return {
            "tournament_name": self.tournament_name,
            "location": self.location,
            "tournament_date_begin": self.tournament_date_begin,
            "tournament_date_end": self.tournament_date_end,
            "number_of_round": self.number_of_round,
            "players_choice": self.players_choice,
            "time_controller_choice": self.time_controller_choice,
            "description": self.description,
            "round_ids": self.round_ids,
            "id": self.id,
        }

    # allow to set data in instance
    def unset_data(self, data):
        tournament_name: str = data["tournament_name"]
        location: str = data["location"]
        tournament_date_begin: str = data["tournament_date_begin"]
        tournament_date_end: str = data["tournament_date_end"]
        number_of_round: int = data["number_of_round"]
        players_choice: list = data["players_choice"]
        time_controller_choice: str = data["time_controller_choice"]
        description: str = data["description"]
        round_ids: list = data["round_ids"]
        id: int = data["id"]

        return Tournament(
            tournament_name,
            location,
            tournament_date_begin,
            tournament_date_end,
            number_of_round,
            players_choice,
            time_controller_choice,
            description,
            round_ids,
            id,
        )

    def save(self, tournament_data):
        new_tournament_id = self.table.insert(
            {
                "tournament_name": tournament_data[0],
                "location": tournament_data[1],
                "tournament_date_begin": tournament_data[2],
                "tournament_date_end": tournament_data[3],
                "number_of_round": tournament_data[4],
                "players_choice": tournament_data[5],
                "time_controller_choice": tournament_data[6],
                "description": tournament_data[7],
                "round_ids": tournament_data[8],
                "id": tournament_data[9],
            }
        )
        self.table.update({"id": new_tournament_id}, doc_ids=[new_tournament_id])

    def update(self, tournament_data):
        self.table.update(
            {
                "tournament_name": tournament_data["tournament_name"],
                "location": tournament_data["location"],
                "tournament_date_begin": tournament_data["tournament_date_begin"],
                "tournament_date_end": tournament_data["tournament_date_end"],
                "number_of_round": tournament_data["number_of_round"],
                "players_choice": tournament_data["players_choice"],
                "time_controller_choice": tournament_data["time_controller_choice"],
                "round_ids": tournament_data["round_ids"],
                "description": tournament_data["description"],
            },
            Query().id == tournament_data["id"],
        )

    def get_tournament_by_name(self, tournament_name):
        query = db.table("tournaments").search(Query().tournament_name == tournament_name)
        result = {}
        result["tournament_name"] = query[0]["tournament_name"]
        result["location"] = query[0]["location"]
        result["tournament_date_begin"] = query[0]["tournament_date_begin"]
        result["tournament_date_end"] = query[0]["tournament_date_end"]
        result["number_of_round"] = query[0]["number_of_round"]
        result["players_choice"] = query[0]["players_choice"]
        result["time_controller_choice"] = query[0]["time_controller_choice"]
        result["description"] = query[0]["description"]
        result["round_ids"] = query[0]["round_ids"]
        result["id"] = query[0]["id"]

        return result

    def get_tournament_by_id(self, id):
        query = db.table("tournaments").search(Query().id == int(id))
        result = {}
        result["tournament_name"] = query[0]["tournament_name"]
        result["location"] = query[0]["location"]
        result["tournament_date_begin"] = query[0]["tournament_date_begin"]
        result["tournament_date_end"] = query[0]["tournament_date_end"]
        result["number_of_round"] = query[0]["number_of_round"]
        result["players_choice"] = query[0]["players_choice"]
        result["time_controller_choice"] = query[0]["time_controller_choice"]
        result["description"] = query[0]["description"]
        result["round_ids"] = query[0]["round_ids"]
        result["id"] = query[0]["id"]

        return result

    def display_tournament_data(self, tournament_id=None):
        if tournament_id:
            in_db = Query()
            return db.table("tournaments").get(in_db.id == tournament_id)
        else:
            return db.table("tournaments").all()

    def check_id(self, id):
        in_db = Query()
        if len(db.table("tournaments").search(in_db.id == id)):
            return True
        else:
            return False

    def __str__(self):
        return f"{self.tournament_name} a lieu à {self.location}"


class Tour(Table):
    NUMBER_OF_TOUR = 1

    def __init__(
        self,
        time_begin=None,
        time_end=None,
        list_of_completed_matchs=None,
    ):
        self.table = "tour"
        self.id = 0
        self.name: str = f"Tour {str(Tour.NUMBER_OF_TOUR)}"
        self.time_begin: str = time_begin
        self.time_end: str = time_end
        self.list_of_completed_matchs: list = list_of_completed_matchs
        self.table = db.table(self.table)

    # allow editing.
    def set_data(self):
        return {
            "time_begin": self.time_begin,
            "time_end": self.time_end,
            "list_of_completed_matchs": self.list_of_completed_matchs,
        }

    # allow to set data in instance
    def unset_data(self, data):
        time_begin = data["time_begin"]
        time_end = data["time_end"]
        list_of_completed_matchs = data["list_of_completed_matchs"]

        Tour(time_begin, time_end, list_of_completed_matchs)

    def save(self, tour_data):
        new_tour_id = self.table.insert(
            {
                "id": 0,
                "name": self.name,
                "time_begin": tour_data["time_begin"],
                "time_end": tour_data["time_end"],
                "list_of_completed_matchs": tour_data["list_of_completed_matchs"],
            }
        )
        self.table.update({"id": new_tour_id}, doc_ids=[new_tour_id])

    def get_tour_id(self, tour_data):
        in_db = Query()
        return self.table.get(
            (in_db.time_begin == tour_data["time_begin"])
            & (in_db.time_end == tour_data["time_end"])
            & (in_db.list_of_completed_matchs == tour_data["list_of_completed_matchs"])
        ).doc_id

    def up_turn_number(self):
        Tour.NUMBER_OF_TOUR += 1
        return Tour.NUMBER_OF_TOUR

    def get_time_now(self):
        datetime_paris = datetime.now(pytz.timezone("Europe/Paris"))
        return datetime_paris.strftime("%d-%m-%y à %H:%M:%S")


class Match(Table):
    NUMBER_OF_MATCH = 0

    def __init__(self, player_1: Player = None, player_2: Player = None, score_player_1=0.0, score_player_2=0.0):
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2

    def up_match_number(self):
        Match.NUMBER_OF_MATCH += 1
        return Match.NUMBER_OF_MATCH
