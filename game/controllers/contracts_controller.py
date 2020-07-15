#from game.config import *
from copy import deepcopy
import random

from game.utils.helpers import write_json_file
from game.common.action import Action
from game.controllers.controller import Controller

from game.common.node import Node
from game.common.map import Map
from game.common.contract import Contract
from game.common.truck import Truck
from game.common.player import Player


class ContractController(Controller):

    def __init__(self):
        super().__init__()
        self.contract_list = []
        self.selected_contract = None

    def get_contracts(self):
        return self.contract_list
    
    def generate_contracts(self, client):
        currMap = Map.getData()
        cityList = []
        hub = None
        for city in currMap['cities']:
            if city.location_type == client.truck.current_node.location_type:
                cityList.append(city)
        for city in currMap['cities']:
            if city.city_name.lower().find('hub') != -1:
                hub = city

        contractList = [
                Contract(None, client.truck.current_node.location_type, [hub, random.choice(cityList)]),
                Contract(None, client.truck.current_node.location_type, [hub, random.choice(cityList)]),
                Contract(None, client.truck.current_node.location_type, [hub, random.choice(cityList)])]
        
        self.contract_list = contractList

    def handle_actions(self, client, player):
        # Player is updated to conform to design guidelines in instruction book
        player.action.contract_list = deepcopy(self.contract_list)
        player.contracts = deepcopy(self.contract_list)
        if client.action._example_action is ActionType.select_contract:
            if 0 < int(client.contractID) < len(self.contract_list):
                self.selected_contract = [self.contract_list.pop(int(client.contractID))]
