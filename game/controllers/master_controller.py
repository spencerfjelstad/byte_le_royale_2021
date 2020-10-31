import copy
from copy import deepcopy

from game.common.action import Action
from game.common.enums import *
from game.common.player import Player
import game.config as config
from game.utils.thread import CommunicationThread

from game.controllers.controller import Controller
from game.controllers.action_controller import ActionController
from game.utils.CreateMap import *
from game.common.truck import Truck
from game.utils.contract_utils import *

import random


class MasterController(Controller):
    def __init__(self):
        super().__init__()
        self.game_over = False
                
        self.turn = None
        self.current_world_data = None
        generateMap()

        self.action_controller = ActionController()

    # Receives all clients for the purpose of giving them the objects they will control
    def give_clients_objects(self, client):
        client.truck = Truck("HUB")
        pass

    # Generator function. Given a key:value pair where the key is the identifier for the current world and the value is
    # the state of the world, returns the key that will give the appropriate world information
    def game_loop_logic(self, start=1):
        self.turn = start

        # Basic loop from 1 to max turns
        while True:
            # Wait until the next call to give the number
            yield self.turn
            # Increment the turn counter by 1
            self.turn += 1
            if self.turn > config.MAX_TICKS:
                    break

    # Receives world data from the generated game log and is responsible for interpreting it
    def interpret_current_turn_data(self, client, world, turn):
        self.current_world_data = world
        self.subtract_time(world["time_taken"])

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client, turn):
        # Add contracts available in city and current active contract to truck for access by client
        actions = Action()
        
        contract_list = contract_utils.generate_contracts(client)
        self.action_controller.contract_list = contract_list

        client.truck.contract_list = copy.deepcopy(contract_list)
        client.truck.active_contract = copy.deepcopy(client.active_contract)
        client.action = actions



        # Create deep copies of all objects sent to the player

        #Truck obfuscation
        truckCopy = copy.deepcopy(client.truck)
        truckCopy.obfuscate()
        truckCopy.current_node.obfuscate()
        for contract in truckCopy.contract_list:
            contract.obfuscate()

        #Time copy to be given to player
        timeCopy = copy.deepcopy(client.time)
        timeCopy.obfuscate()
        
        # Obfuscate data in objects that that player should not be able to see
        args = (self.turn, actions, self.current_world_data, truckCopy, timeCopy)
        return args

    # Perform the main logic that happens per turn
    def turn_logic(self, client, turn):
        random.seed(self.current_world_data["seed"])

        self.action_controller.handle_actions(client)

        if client.time <= 0:
            self.print("Game is ending because time has run out.")
            self.game_over = True

    # Return serialized version of game
    def create_turn_log(self, clients, turn):
        data = dict()

        # Add things that should be thrown into the turn logs here
        data['temp'] = None

        return data

    # Gather necessary data together in results file
    def return_final_results(self, client, turn):
        data = dict()

        # Determine results
        data['player'] = client.to_json()

        return data
    

    ##ERROR. Should be a util in the utils folder
    def subtract_time(self,time):
        self.time -= abs(time)
