import os
import sys
from enum import Enum
if os.path.basename(__file__) != 'main.py':
    PROJECT_CWD = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1])
else:
    PROJECT_CWD = f"{os.sep}".join(os.getcwd().split(os.sep))
sys.path.append(PROJECT_CWD)
sys.path.append(os.path.join(PROJECT_CWD,"models"))
sys.path.append(os.path.join(PROJECT_CWD,"views"))


from models.tables import TimeController, Player, Tournament

class Controller:
    def __init__(self):
        self.time_controller = TimeController
        self.player_controller = Player()
        self.tournament_controller = Tournament()
    def check_enum_status(self, input:str):
        if input in self.time_controller._value2member_map_:
            return True
    def get_players_list(self):
        return self.player_controller.display_data()
    def get_tournament_list(self):
        return self.tournament_controller.display_data()
    def save_tournament(self, data:dict):
        new_tournament = Tournament(data)
        return new_tournament.save()
    def save_player(self, data:dict):
        new_player = Player(data)
        return new_player.save()