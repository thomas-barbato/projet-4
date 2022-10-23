from tinydb import TinyDB, Query
from datetime import datetime
from enum import Enum

db = TinyDB("db_chess.json")


class Player:
    def __init__(
        self,
        last_name: str,
        first_name: str,
        date_of_birth: str,
        gender: str,
        age: int,
        ranking: int,
    ):
        self.last_name: str = last_name
        self.first_name: str = first_name
        self.date_of_birth: str = date_of_birth
        self.gender: str = gender
        self.age: str = age
        self.ranking: int = ranking
        self.players_table: str = db.table("players")
        self.serialized_players: dict = {
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
        name: str,
        location: str,
        date: str,
        number_of_turn: int,
        players: list,
        time_controller: str,
        description: str = "",
    ):
        self.name = name
        self.location = location
        self.date = date
        self.number_of_turn = number_of_turn
        self.players = players
        self.time_controller = (
            time_controller
            if time_controller in TimeController._value2member_map_
            else "Empty"
        )
        self.description = description
        self.tournaments_table: str = db.table("tournaments")
        self.serialized_tournaments: dict = {
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


x = Player("a", "b", "10/09/1989", "male", 15, 3)
x.save()
x = Player("x", "e", "12/03/1983", "male", 22, 2)
x.save()

print(x.display_data())
print(x.clear_table())
print(x.display_data())

# check if "blitz" is in TimeController
print("blitz" in TimeController._value2member_map_)
