from tinydb import TinyDB, Query
from datetime import datetime
from enum import Enum
import os
import sys

# used to unallow writing db_chess.json anywhere but in tables.py
DIR = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1]) + os.sep + "models" + os.sep + "db_chess.json"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
db = TinyDB(os.path.join(ROOT_DIR,"db_chess.json"))


class Player:
    def __init__(
        self,
        data: dict = {}
    ):
        if data:
            self.last_name: str = data['last_name']
            self.first_name: str = data['first_name']
            self.date_of_birth: str = data['date_of_birth']
            self.gender: str = data['gender']
            self.age: int = data['age']
            self.ranking: int = data['ranking']
            self.players_table: str = db.table("players")
            self.serialized_players: dict = {
                "id": len(self.players_table),
                "last_name": self.last_name,
                "first_name": self.first_name,
                "date_of_birth": self.date_of_birth,
                "gender": self.gender,
                "age": self.age,
                "ranking": self.ranking,
            }

    def __get_serialized_player(self):
        return self.serialized_players

    def save(self):
        self.players_table.insert_multiple([self.__get_serialized_player()])

    def display_data(self):
        return db.table("players").all()

    def clear_table(self):
        db.table("players").truncate()


class TimeController(Enum):
    BULLET = "bullet"
    BLITZ = "blitz"
    COUP_RAPIDE = "coup_rapide"


class Tournament:
    def __init__(
        self,
        data: dict = {}
    ):
        if data:
            self.tournament_name: str = data['tournament_name']
            self.location: str = data['location']
            self.tournament_date_begin: str = data['tournament_date_begin']
            self.tournament_date_end: str = data['tournament_date_end']
            self.number_of_turn: int = data['number_of_turn']
            self.number_of_round: int = data['number_of_round']
            self.players_list: dict = data['players_list']
            self.time_controller_choice: str = (
                data['time_controller_choice']
                if data['time_controller_choice'] in TimeController._value2member_map_
                else "Empty"
            )
            self.description: str = data['description']
            
            self.tournaments_table: str = db.table("tournaments")
            self.serialized_tournaments: dict = {
                "id": len(self.tournaments_table),
                "name": self.tournament_name,
                "location": self.location,
                "tournament_date_begin": self.tournament_date_begin,
                "tournament_date_end": self.tournament_date_end,
                "number_of_turn": self.number_of_turn,
                "number_of_round": self.number_of_round,
                "players_list": self.players_list,
                "time_controller_choice": self.time_controller_choice,
                "description": self.description,
            }

    def __get_serialized_tournaments(self):
        return self.serialized_tournaments

    def save(self):
        self.tournaments_table.insert_multiple([self.__get_serialized_tournaments()])

    def display_data(self):
        return db.table("tournaments").all()

    def clear_table(self):
        db.table("tournaments").truncate()



x = Player({"first_name": "thomas", "last_name": "barbato", "date_of_birth": "10/09/1989", "gender": "male", "age":33, "ranking": 3})
x.save()
x = Player({"first_name": "benois", "last_name": "de bondt", "date_of_birth": "29/08/1985", "gender": "male", "age":37, "ranking": 2})
x.save()
