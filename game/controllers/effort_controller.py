from game.common.stats import GameStats
from game.common.building import Building
from game.common.city import City
from game.common.disasters import LastingDisaster
from game.common.player import Player
from game.common.sensor import Sensor
from game.controllers.controller import Controller
from game.controllers.event_controller import EventController
from game.config import *
from game.utils.helpers import clamp, enum_iter

from collections import deque
import math


class EffortController(Controller):
    def __init__(self):
        super().__init__()
        self.event_controller = EventController.get_instance()

    def handle_actions(self, player):
        # handle advanced verification of allocation list
       
    # Sorts the allocations in order they should be processed
    # e.g. homes (structure) should be repaired before new people (population) are generated
    @staticmethod
    def __sort_allocations(allocation):
        act, amount = allocation
        try:
            if act in enum_iter(ActionType):
                return GameStats.action_sort_order[act]
            else:
                return GameStats.object_sort_order[act.object_type]
        except KeyError as e:
            print("SYSTEM EXCEPTION: Game object passed to the allocation list was not included in the sort order.")
            print("If you are receiving this error, please let Wyly know.")
            raise e
