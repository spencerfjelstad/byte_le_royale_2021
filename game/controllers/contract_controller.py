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
        self.map_distances = {}
        # Arbitrary placeholder bounds
        self.easy_distance = 10
        self.medium_distance = 20
        self.hard_distance = 30

        self.easy_reward = 100
        self.medium_reward = 225
        self.hard_reward = 325
    
    # Generate list of contracts, store for verification
    def generate_contracts(self, client):
        self.world_distances(client.truck.current_node)
        curr_map = Map.getData()
        city_list = []
        easy_list = {}
        medium_list = {}
        hard_list = {}
        hub = None
        for city in curr_map['cities']:
            if city.region == client.truck.current_node.region:
                city_list.append(city)
        for city in curr_map['cities']:
            if 'hub' in city.city_name.lower():
                hub = city

        for city in self.map_distances:
            distance = self.map_distances[city]
            if distance <= 10:
                easy_list[city] = int((distance/self.easy_distance)*self.easy_reward)
            elif distance <= 20:
                medium_list[city] = int((distance/self.medium_distance)*self.medium_reward)
            else:
                hard_list[city] = int((distance/self.hard_distance)*self.hard_reward)

        # Placeholder contract generation
        easy_city = random.choice(easy_list)
        medium_city = random.choice(medium_list)
        hard_city = random.choice(hard_list)
        contract_list = [
                Contract(None, client.truck.current_node.region, [hub, easy_city],
                    self.easy_list[easy_city]),
                Contract(None, client.truck.current_node.region, [hub, medium_city],
                    self.medium_list[medium_city]),
                Contract(None, client.truck.current_node.region, [hub, hard_city],
                    self.hard_list[hard_city])]
        
        self.contract_list = contract_list

    def world_distances(self, node):
        map = Map.getData()
        unvisited = {city.city_name: None for city in map['cities']}
        visited = {}
        curr_distance = 0
        curr_city = node
        unvisited[curr_city.city_name] = curr_distance
        while True:
            for connection in curr_city.connections:
                path = curr_city.get_connection(Map.getRoadByName(connection))
                if path['city'] not in unvisited:
                    continue
                new_distance = curr_distance + path['type']
                if unvisited[path['city']] is None or unvisited[path['city']] > new_distance:
                    unvisited[path['city']] = new_distance
                visited[curr_city.city_name] = curr_distance
                del unvisited[curr_city.city_name]
                if not unvisited:
                    break
                candidates = [node for node in unvisited.items() if node[1] is not None]
                curr_city, curr_distance = sorted(candidates, key=lambda x: x[1])[0]

        sorted_distances = {k: v for k, v in sorted(visited.items(), key=lambda item: item[1])}
        self.map_distances = sorted_distances

    # If contract was selected retrieve by index and store in Player, then clear the list
    def handle_actions(self, client):
        if client.action._chosen_action is ActionType.select_contract:
            client.active_contract = self.contract_list[int(client.action.contract_index)]
            self.contract_list.clear()
        elif (client.action._chosen_action is ActionType.complete_contract and
                client.active_contract.cities[1] == client.truck.current_node):
            client.money += client.active_contract.reward
            client.active_contract = None
