from game.common.enums import *
from game.config import Debug
import copy


class UserClient:
    def __init__(self):
        self.truck = copy.deepcopy(truck)
        self.debug_level = DebugLevel.client
        self.debug = True

    def print(self, *args):
        if self.debug and Debug.level >= self.debug_level:
            print(f'{self.__class__.__name__}: ', end='')
            print(*args)

    def team_name(self):
        return "No_Team_Name_Available"

    def take_turn(self, turn, actions, world, truck, time):
        raise NotImplementedError("Implement this in subclass")
