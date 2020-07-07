from game.common.enums import *

from game.common.node import Node
from game.common.map import Map
from game.common.contract import Contract
from game.common.truck import Truck
from game.common.player import Player

class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self.contract_list = []
        self._example_action = None

    def set_action(self, action):
        self._example_action = action

    def generate_contracts(self):
        # Not sure if this functionality should be handled elsewhere, but needed to be able to call this during tick
        currMap = Map.getData()
        cityList = []
        for city in currMap['cities']:
            if city.location_type == truck.current_node.location_type:
                cityList.append(city)
        contractList = [Contract(None, truck.current_node.location_type, [random.choice(cityList), random.choice(cityList)]),
                Contract(None, truck.current_node.location_type, [random.choice(cityList), random.choice(cityList)]), 
                Contract(None, truck.current_node.location_type, [random.choice(cityList), random.choice(cityList)])]
            
        self.contract_list = contractList

    def select_contract(self,contractID):
        # Currently interacts with list through index to avoid fake contracts being passed
        if contractID < len(player.contracts) and contractID > 0:
            self.contract_list = [self.contract_list.pop(contractID)]

    def to_json(self):
        data = dict()

        data['object_type'] = self.object_type
        data['example_action'] = self._example_action

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._example_action = data['example_action']

    def __str__(self):
        outstring = ''
        outstring += f'Example Action: {self._example_action}\n'

        return outstring


