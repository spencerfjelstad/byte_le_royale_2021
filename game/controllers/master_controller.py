import copy
from copy import deepcopy

import game.config as config
from game.common.action import Action
from game.common.enums import *
from game.common.player import Player
from game.common.node import Node
from game.utils.thread import CommunicationThread
from game.controllers.action_controller import ActionController
from game.controllers.controller import Controller
from game.common.truck import Truck
from game.utils.contract_utils import generate_contracts, check_contract_completion
from game.common.game_map import Game_Map

import random


class MasterController(Controller):
    def __init__(self):
        super().__init__()
        self.game_over = False

        self.turn = None
        self.current_world_data = None

        self.action_controller = ActionController()

    # Receives all clients for the purpose of giving them the objects they will control
    def give_clients_objects(self, client):
        client.truck = Truck()
        node = Node('Start Node')
        game_map = Game_Map(node)
        client.truck.map = game_map
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

    # Receive a specific client and send them what they get per turn. Also obfuscates necessary objects.
    def client_turn_arguments(self, client, turn):
        # Add contracts available in city and current active contract to truck for access by client
        actions = Action()
        check_contract_completion(client)
        contract_list = generate_contracts(client)
        self.action_controller.contract_list = contract_list

        client.truck.contract_list = copy.deepcopy(contract_list)
        client.action = actions



        # Create deep copies of all objects sent to the player

        #Truck obfuscation
        truckCopy = copy.deepcopy(client.truck)
        truckCopy.obfuscate()

        #Time copy to be given to player
        timeCopy = copy.deepcopy(client.time)

        # Obfuscate data in objects that that player should not be able to see
        args = (self.turn, actions, self.current_world_data, truckCopy, timeCopy)
        return args

    selected_action = ActionType.none
    selected_route = RoadType.none
    event = EventType.none
    # Perform the main logic that happens per turn
    def turn_logic(self, client, turn):
        random.seed(self.current_world_data["seed"])

        new_action = self.action_controller.handle_actions(client)
        if len(str(new_action)) > 1:
            self.selected_action = new_action[0]
            self.selected_route = new_action[1]
            self.event = new_action[2]
        else:
            self.selected_action = new_action
        #client.time -= 10
        if client.time <= 0:
            print("Game is ending because time has run out. Final score is " + str(client.truck.renown))
            self.game_over = True
        if client.truck.health <= 0:
            print("Game is ending because health has run out. Final score is " + str(client.truck.renown))
            self.game_over = True
        if client.truck.body.current_gas <= 0:
            print("Game is ending because gas has run out. Final score is " + str(client.truck.renown))
            self.game_over = True

    # Return serialized version of game
    def create_turn_log(self, clients, turn):
        data = dict()
        # Add things that should be thrown into the turn logs here
        data['Team Name'] = clients.team_name
        data['time'] = clients.time
        data['truck'] = clients.truck.to_json()
        data['selected_action'] = self.selected_action
        data['selected_route'] = self.selected_route
        data['event'] = self.event
        
        return data

    # Gather necessary data together in results file
    def return_final_results(self, client, turn):
        data = dict()

        # Determine results
        data['player'] = client.to_json()

        return data
