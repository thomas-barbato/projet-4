import os
import sys
PROJECT_CWD = f"{os.sep}".join(os.getcwd().split(os.sep)[:-1])
print(PROJECT_CWD)
sys.path.append(PROJECT_CWD)
sys.path.append(os.path.join(PROJECT_CWD,"models"))
sys.path.append(os.path.join(PROJECT_CWD,"views"))

print(sys.path)

from models.tables import TimeController, Player, Tournament

class Engine:
    def __init__(self):
        pass
        self.timeController = TimeController()
    def get_time_controller(self):
        return self.timeController
    
print(TimeController)