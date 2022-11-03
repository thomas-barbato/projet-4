"""import"""
from tinydb import TinyDB
from enum import Enum

db = TinyDB("db_chess.json")


class Table:
    def __init__(self, data: dict = {}, table_name: str = ""):
        self.table = ""

    def __get_serialized_data(self):
        return self.serialized_data

    def save(self):
        self.table.insert_multiple([self.__get_serialized_data()])

    def display_data(self):
        return db.table(self.table).all()

    def clear_table(self):
        db.table(self.table).truncate()


class Player(Table):
    def __init__(self, data: dict = {}):
        self.table = "players"
        if data:
            self.last_name: str = data["last_name"]
            self.first_name: str = data["first_name"]
            self.date_of_birth: str = data["date_of_birth"]
            self.gender: str = data["gender"]
            self.age: int = data["age"]
            self.ranking: int = data["ranking"]
            self.table: str = db.table(self.table)
            self.score: float = 0.0
            self.serialized_data: dict = {
                "id": len(self.table),
                "last_name": self.last_name,
                "first_name": self.first_name,
                "date_of_birth": self.date_of_birth,
                "gender": self.gender,
                "age": self.age,
                "ranking": self.ranking,
                "score": self.score,
        }

    def __str__(self):
        return f"{self.first_name} {self.last_name} est classé {self.ranking}\
            avec score de {self.score}"

class TimeController(Enum):
    BULLET = "bullet"
    BLITZ = "blitz"
    COUP_RAPIDE = "coup_rapide"


class Tournament(Table):
    def __init__(self, data: dict = {}):
        self.table = "tournaments"
        if data:
            self.tournament_name: str = data["tournament_name"]
            self.location: str = data["location"]
            self.tournament_date_begin: str = data["tournament_date_begin"]
            self.tournament_date_end: str = data["tournament_date_end"]
            self.number_of_turn: int = data["number_of_turn"]
            self.number_of_round: int = data["number_of_round"]
            self.players_choice: dict = data["players_choice"]
            self.time_controller_choice: str = (
                data["time_controller_choice"]
                if data["time_controller_choice"] in TimeController._value2member_map_
                else "Empty"
            )
            self.description: str = data["description"]
            self.table: str = db.table(self.table)
            self.serialized_data: dict = {
                "id": len(self.table),
                "name": self.tournament_name,
                "location": self.location,
                "tournament_date_begin": self.tournament_date_begin,
                "tournament_date_end": self.tournament_date_end,
                "number_of_turn": self.number_of_turn,
                "number_of_round": self.number_of_round,
                "players_choice": self.players_choice,
                "time_controller_choice": self.time_controller_choice,
                "description": self.description,
                }
    def __str__(self):
        return f"{self.tournament_name}"

class Tour(Table):
    matches = []
    def __init__(self, data):
        self.table = "tour"
        self.turn_name: str = data['turn_name']
        self.ronde_instance: list = data['ronde_instance']
        self.time_begin: str = data['time_begin']
        self.time_end: str = data['time_end']
        self.table: str = db.table(self.table)
        self.serialized_data: dict = {
            "turn_name" : self.turn_name,
            "ronde_instance": self.ronde_instance,
            "time_begin": self.time_begin,
            "time_end": self.time_end
        }

if len(db.table("players")) < 8:
    x = Player(
        {
            "first_name": "Belian",
            "last_name": "Maieslav",
            "date_of_birth": "10/09/1989",
            "gender": "male",
            "age": 33,
            "ranking": 2,
        }
    )
    x.save()
    x = Player(
        {
            "first_name": "Deirdre",
            "last_name": "De Lothlorien",
            "date_of_birth": "10/09/1989",
            "gender": "female",
            "age": 34,
            "ranking": 1,
            "score": 0
        }
    )
    x.save()
    x = Player(
        {
            "first_name": "Cole",
            "last_name": "Forhman",
            "date_of_birth": "29/08/1985",
            "gender": "male",
            "age": 37,
            "ranking": 4,
            "score": 0
        }
    )
    x.save()
    x = Player(
        {
            "first_name": "Case",
            "last_name": "Gibson",
            "date_of_birth": "29/08/1985",
            "gender": "male",
            "age": 37,
            "ranking": 5,
            "score": 0
        }
    )
    x.save()
    x = Player(
        {
            "first_name": "Billy",
            "last_name": "Bob",
            "date_of_birth": "29/08/1985",
            "gender": "male",
            "age": 22,
            "ranking": 2,
            "score": 0
        }
    )
    x.save()
    x = Player(
        {
            "first_name": "Thomas",
            "last_name": "Barbato",
            "date_of_birth": "10/08/1989",
            "gender": "male",
            "age": 33,
            "ranking": 1,
            "score": 0
        }
    )
    x.save()
    x = Player(
        {
            "first_name": "Benoît",
            "last_name": "De Bondt",
            "date_of_birth": "18/06/1965",
            "gender": "male",
            "age": 63,
            "ranking": 4,
            "score": 0
        }
    )
    x.save()
    x = Player(
        {
            "first_name": "Yue",
            "last_name": "San",
            "date_of_birth": "10/08/1990",
            "gender": "female",
            "age": 32,
            "ranking": 4,
            "score": 0
        }
    )
    x.save()
