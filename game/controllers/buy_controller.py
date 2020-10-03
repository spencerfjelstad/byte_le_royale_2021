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


class buyController(Controller):

    def __init__(self):
        super().__init__()
    
    # Generate list of contracts, store for verification
    def buy_gas(self, client, percentGas = 1):
        if(client.truck.current_node.node_type is )



    def give_money(self, client, money):
        client.truck.money += money

    # If contract was selected retrieve by index and store in Player, then clear the list
    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.select_contract:
            client.active_contract = self.contract_list[int(client.action.contract_index)]
            self.contract_list.clear()


