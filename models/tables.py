"""import"""
from tinydb import TinyDB, Query, where
from datetime import datetime
from enum import Enum
import os

# used to unallow writing db_chess.json anywhere but in tables.py
if os.path.basename(__file__) != "main.py":
    DIR = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1]) + os.sep + "db_chess.json"
else:
    DIR = f"{os.sep}".join(os.getcwd().split(os.sep)) + os.sep + "db_chess.json"

db = TinyDB(os.path.join(DIR))


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
            self.serialized_data: dict = {
                "id": len(self.table),
                "last_name": self.last_name,
                "first_name": self.first_name,
                "date_of_birth": self.date_of_birth,
                "gender": self.gender,
                "age": self.age,
                "ranking": self.ranking,
            }


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
            self.players_list: dict = data["players_list"]
            self.time_controller_choice: str = (
                data["time_controller_choice"]
                if data["time_controller_choice"] in TimeController._value2member_map_
                else "Empty"
            )
            self.description: str = data["description"]
            self.pairing: dict = {}

            self.table: str = db.table(self.table)
            self.serialized_data: dict = {
                "id": len(self.table),
                "name": self.tournament_name,
                "location": self.location,
                "tournament_date_begin": self.tournament_date_begin,
                "tournament_date_end": self.tournament_date_end,
                "number_of_turn": self.number_of_turn,
                "number_of_round": self.number_of_round,
                "players_list": self.players_list,
                "time_controller_choice": self.time_controller_choice,
                "description": self.description,
                "pairing": self.pairing,
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
        }
    )
    x.save()

# in_db = Query()
# print(db.table("players").search(in_db.id != 2))
