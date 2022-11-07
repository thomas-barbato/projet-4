"""import"""
from tinydb import TinyDB, Query
from enum import Enum

db = TinyDB("db_chess.json")


class Table:
    def __init__(self, data: dict = {}, table_name: str = ""):
        self.table = ""

    def display_data(self):
        return db.table(self.table).all()

    def clear_table(self):
        db.table(self.table).truncate()

    def get_id_list(self):
        return [id.doc_id for id in db.table(self.table)]


class Player(Table):
    def __init__(
        self,
        first_name=None,
        last_name=None,
        date_of_birth=None,
        gender=None,
        ranking=None,
        score=None,
        id=None
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

    def set_data(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "ranking": self.ranking,
            "score": self.score,
            "id": self.id,
        }

    def get_data(self):
        return Player(
            self.set_data()["last_name"],
            self.set_data()["first_name"],
            self.set_data()["date_of_birth"],
            self.set_data()["gender"],
            self.set_data()["ranking"],
            self.set_data()["score"],
            self.set_data()["id"],
        )

    def save(self, player_data):
        new_player = Player(
            player_data[0],  
            player_data[1], 
            player_data[2], 
            player_data[3], 
            player_data[4], 
            player_data[5], 
            player_data[6],   
        )
        new_player_id = self.table.insert({
            "first_name": player_data[0],
            "last_name": player_data[1],
            "date_of_birth": player_data[2],
            "gender": player_data[3],
            "ranking": player_data[4],
            "score": player_data[5],
            "id": player_data[6]
        })
        self.table.update({"id": new_player_id }, doc_ids=[new_player_id])
        
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
    ):
        self.table = "tournaments"
        self.tournament_name: str = tournament_name
        self.location: str = location
        self.tournament_date_begin: str = tournament_date_begin
        self.tournament_date_end: str = tournament_date_end
        self.number_of_round: int = number_of_round
        self.players_choice = players_choice
        self.time_controller_choice: str = time_controller_choice
        self.description: str = description
        self.id = 0
        self.table = db.table(self.table)
    
    def set_data(self):
        return {
            "tournament_name": self.tournament_name,
            "location": self.location,
            "tournament_date_begin": self.tournament_date_begin,
            "tournament_date_end": self.tournament_date_end,
            "number_of_round": self.number_of_round,
            "time_controller_choice": self.time_controller_choice,
            "players_choice": self.players_choice,
            "description": self.description,
            "id": self.id,
        }

    def get_data(self):
        return Tournament(
            self.set_data()["tournament_name"],
            self.set_data()["location"],
            self.set_data()["tournament_date_begin"],
            self.set_data()["tournament_date_end"],
            self.set_data()["number_of_round"],
            self.set_data()["time_controller_choice"],
            self.set_data()["players_choice"],
            self.set_data()["description"],
            self.set_data()["id"],
        )

    def save(self, tournament_data):
        new_tournament = Tournament(
            tournament_data[0],
            tournament_data[1],
            tournament_data[2],
            tournament_data[3],
            tournament_data[4],
            tournament_data[5],
            tournament_data[6],
            tournament_data[7],
            tournament_data[8], 
        )
        new_tournament_id = self.table.insert({
            "tournament_name": tournament_data[0],
            "location": tournament_data[1],
            "tournament_date_begin": tournament_data[2],
            "tournament_date_end": tournament_data[3],
            "number_of_round": tournament_data[4],
            "players_choice": tournament_data[5],
            "time_controller_choice": tournament_data[6],
            "description": tournament_data[7],
            "id": tournament_data[8]
            })
        self.table.update({"id": new_tournament_id }, doc_ids=[new_tournament_id])
        

    def __str__(self):
        return f"{self.tournament_name}"


class Tour(Table):
    def __init__(self, data):
        self.table = "tour"
        self.tournament_id: int = 0
        self.ronde_instance: tuple = ()
        self.time_begin: str = data["time_begin"]
        self.time_end: str = data["time_end"]
        self.table = db.table(self.table)
        self.serialized_data: dict = {
            "turn_id": self.tournament_id,
            "ronde_instance": self.ronde_instance,
            "time_begin": self.time_begin,
            "time_end": self.time_end,
        }


class Match(Table):
    """
    Un match unique doit être stocké sous la forme d'un tuple contenant deux listes,
    chacune contenant deux éléments : une référence à une instance de joueur et un score.
    Les matchs multiples doivent être stockés sous forme de liste sur l'instance du tour.
    """

    NUMBER_OF_MATCH = 1

    def __init__(self, player_1: Player = None, player_2: Player = None, score_player_1=0, score_player_2=0):
        self.name = "Match numéro: " + str(Match.NUMBER_OF_MATCH)
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2

    def __str__(self):
        return f"[{self.name}] Compétiteurs : {self.player_1},  {self.player_2}."

    def up_match_number(self):
        Match.NUMBER_OF_MATCH += 1



