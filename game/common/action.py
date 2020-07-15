from game.common.enums import *

from game.common.node import Node
from game.common.map import Map
from game.common.contract import Contract
from game.common.truck import Truck
from game.common.player import Player

import random


class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self.contract_list = []
        self._example_action = None

    def set_action(self, action):
        self._example_action = action
    
    def to_json(self):
        data = dict()

        data['object_type'] = self.object_type
        data['example_action'] = self._example_action
        data['contract_list'] = self.contract_list

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._example_action = data['example_action']
        self.contract_list = data['contract_list']

    def __str__(self):
        outstring = ''
        outstring += f'Example Action: {self._example_action}\n'

        return outstring


