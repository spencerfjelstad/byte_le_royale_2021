#from game.config import *
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
        self.contracts
# Currently moving this functionality out of the controller
#    def generateContracts(self, player, truck):
#        currMap = Map.getData()
#        cityList = []
#        for city in currMap['cities']:
#            if city.location_type == truck.current_node.location_type:
#                cityList.append(city)
#        contractList = [Contract(None, truck.current_node.location_type, [random.choice(cityList), random.choice(cityList)]),
#                Contract(None, truck.current_node.location_type, [random.choice(cityList), random.choice(cityList)]), 
#                Contract(None, truck.current_node.location_type, [random.choice(cityList), random.choice(cityList)])]
#            
#        return contractList

#    def selectContract(self, player, selectedContract):
#        player.contracts.append(selectedContract)


    def handle_actions(self, client, player, action):
#        if client.action._chosen_action is ActionType.getContracts and len(player.contracts) == 0:
#            player.contracts = generateContracts(client.truck)
#        elif client.action._chosen_action is ActionType.selectContract:
#            selectContract(truck, contract)
        player.contracts = action.contract_list
