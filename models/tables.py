from tinydb import TinyDB, Query
from datetime import datetime
from enum import Enum

db = TinyDB("db_chess.json")


class Player:
    def __init__(
        self,
        data: dict
    ):
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
        data: dict,
    ):
        self.name: str = data['name']
        self.location: str = data['location']
        self.date: str = data['date']
        self.number_of_turn: int = data['number_of_turn']
        self.players: dict = data['players']
        self.time_controller: str = (
            data['time_controller']
            if data['time_controller'] in TimeController._value2member_map_
            else "Empty"
        )
        self.description: str = data[' description']
        self.tournaments_table: str = db.table("tournaments")
        self.serialized_tournaments: dict = {
            "id": len(self.tournaments_table),
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "number_of_turn": self.number_of_turn,
            "players": self.players,
            "time_controller": self.time_controller,
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



x = Player({"first_name": "a", "last_name": "b", "date_of_birth": "10/09/1989", "gender": "male", "age":15, "ranking": 3})
x.save()
x = Player({"first_name": "sqxsxqs", "last_name": "dddddd", "date_of_birth": "01/12/1989", "gender": "male", "age":27, "ranking": 4})
x.save()

print(x.display_data())

# check if "blitz" is in TimeController
print("blitz" in TimeController._value2member_map_)
