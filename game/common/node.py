from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *
import random

class Node(GameObject):
    
    def __init__(self, name, roads=[], next_node=None):
        super().__init__()
        self.object_type = ObjectType.node
        self.city_name = name
        self.roads = roads
        self.next_node = next_node
        self.gas_price = round(random.uniform(GameStats.minimum_gas_price, GameStats.maximum_gas_price), 2)  # gas price per percent
<<<<<<< HEAD
        self.repair_price = round(random.uniform(GameStats.minimum_repair_price, GameStats.maximum_repair_price), 2)  # Health price per percent
=======
        self.repair_price = round(random.uniform(GameStats.minimum_health_price, GameStats.maximum_health_price), 2)  # Health price per percent
>>>>>>> 52ba5ffcf4e325c1ff362bfbed688b3911faa8b1
    
    def to_json(self):
        data = super().to_json()
        data['city_name'] = self.city_name
        data['gas_price'] = self.gas_price
        data['repair_price'] = self.repair_price
        data['roads'] = {road.road_name: road.to_json() for road in self.roads}
        data['next_node'] = self.next_node.to_json() if self.next_node is not None else None
        return data

    def from_json(self, data):
        super().from_json(data)
        self.city_name = data['city_name']
        temp = Road('temp')
        for road in data['roads'].values():
            temp.from_json(road)
            self.roads.append(temp)

        # Recursively reconstruct linked list
        node_data = data['next_node']
        if node_data is not None:
            temp_node = Node('temp')
            temp_node.from_json(node_data)
            self.next_node = temp_node

    def to_list(self):
        curr_node = self
        node_list = []
        while curr_node is not None:
            node_list.append(curr_node)
            curr_node = curr_node.next_node
        return node_list
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.city_name == other.city_name
                and self.roads == other.roads and self.next_node == other.next_node)
