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
from game.common.enums import *


class ContractController(Controller):

    def __init__(self):
        super().__init__()
        self.contract_list = []
    
    # Generate list of contracts, store for verification
    def generate_contracts(self, client):
        city_list = []
        hub = None
        for city in Map.cities.values():
            if city.region == Map.getCityByName(client.truck.current_node).region:
                city_list.append(city)
        for city in Map.cities.values():
            if 'hub' in city.city_name.lower():
                hub = city

        # Placeholder contract generation
        contract_list = [
                Contract(None, Map.getCityByName(client.truck.current_node).region, [hub, random.choice(city_list)]),
                Contract(None, Map.getCityByName(client.truck.current_node).region, [hub, random.choice(city_list)]),
                Contract(None, Map.getCityByName(client.truck.current_node).region, [hub, random.choice(city_list)])]
        
        self.contract_list = contract_list

    # If contract was selected retrieve by index and store in Player, then clear the list
    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.select_contract:
            client.active_contract = self.contract_list[int(client.action.contract_index)]
            self.contract_list.clear()
