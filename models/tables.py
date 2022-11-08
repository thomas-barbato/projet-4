"""import"""
from tinydb import TinyDB, Query, where
from enum import Enum

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
        self.ranking: float = score
        self.id = id
        self.table = db.table(self.table)

    def set_data(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "ranking": self.ranking,
            "score": self.ranking,
            "id": self.id,
        }

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
        self.id: int = id
        self.table = db.table(self.table)

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
            "id": self.id,
        }

    # get values from data
    # store them
    # create new Tournament instance
    def unset_data(self, data):
        tournament_name: str = data["tournament_name"]
        location: str = data["location"]
        tournament_date_begin: str = data["tournament_date_begin"]
        tournament_date_end: str = data["tournament_date_end"]
        number_of_round: int = data["number_of_round"]
        players_choice: list = data["players_choice"]
        time_controller_choice: str = data["time_controller_choice"]
        description: str = data["description"]
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
                "id": tournament_data[8],
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
    def __init__(self, name=None, time_begin=None, time_end=None, list_of_completed_matchs=None):
        self.table = "tour"
        self.name: str = name
        self.time_begin: str = time_begin
        self.time_end: str = time_end
        self.list_of_completed_matchs: list = list_of_completed_matchs
        self.table = db.table(self.table)

    def set_data(self):
        return {
            "name": self.name,
            "time_begin": self.time_begin,
            "time_end": self.time_end,
            "list_of_completed_matchs": self.list_of_completed_matchs,
        }

    def unset_data(self, data):
        name = data["name"]
        time_begin = data["time_begin"]
        time_end = data["time_end"]
        list_of_completed_matchs = data["list_of_completed_matchs"]

        Tour(name, time_begin, time_end, list_of_completed_matchs)


class Match(Table):
    def __init__(self, player_1: Player = None, player_2: Player = None, score_player_1=0.0, score_player_2=0.0):
        self.name = f"Match {str(self.up_match_number(Match.NUMBER_OF_MATCH))}"
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2

    def set_data(self):
        return {
            "name": self.name,
            "player_1": self.player_1,
            "player_2": self.player_2,
            "score_player_1": self.score_player_1,
            "score_player_2": self.score_player_2,
        }

    def unset_data(self, data):
        name = data["name"]
        player_1 = data["player_1"]
        player_2 = data["player_2"]
        score_player_1 = data["score_player_1"]
        score_player_2 = data["score_player_2"]

        Match(name, player_1, player_2, score_player_1, score_player_2)

    def up_match_number(self):
        Match.NUMBER_OF_MATCH += 1
        return Match.NUMBER_OF_MATCH

    def __str__(self):
        return f"{self.name} - Compétiteurs : {self.player_1},  {self.player_2}."
