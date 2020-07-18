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


class ContractController(Controller):

    def __init__(self):
        super().__init__()
        self.contract_list = []

    def generate_contracts(self, client):
        currMap = Map.getData()
        cityList = []
        hub = None
        for city in currMap['cities']:
            if city.region == client.truck.current_node.region:
                cityList.append(city)
        for city in currMap['cities']:
            if city.city_name.lower().find('hub') != -1:
                hub = city

        contractList = [
                Contract(None, client.truck.current_node.region, [hub, random.choice(cityList)]),
                Contract(None, client.truck.current_node.region, [hub, random.choice(cityList)]),
                Contract(None, client.truck.current_node.region, [hub, random.choice(cityList)])]
        
        self.contract_list = contractList

        return copy.deepcopy(self.contract_list)

    def handle_actions(self, client):
        # If contract was selected verify it and store in Player
        if client.action._example_action is ActionType.select_contract:
            for c in self.contract_list:
                if c.equals(client.action.contract_list):
                    client.active_contract = client.action._active_contract
                    break
