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

from game.common.enums import NodeType, ActionType


class buyController(Controller):

    def __init__(self):
        super().__init__()
    
    # control gas buying. Either buys the total amount of gas or the max amount allowable
    def buy_gas(self, client):
        gasPrice = random.uniform(1, 5) # gas price per percent
        if(client.truck.current_node.node_type is NodeType.city and client.truck.money > 0):
            percentRemain = 1 - client.truck.gas
            maxPercent =  ( client.truck.money / gasPrice ) / 100
            if(percentRemain < maxPercent):
                client.truck.money -= percentRemain * gasPrice
                client.truck.gas = 1
            else:
                client.truck.money = 0
                client.truck.money += maxPercent

    # If contract was selected retrieve by index and store in Player, then clear the list
    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.buy_gas:
            buy_gas(self, client)


