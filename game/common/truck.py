from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *
from game.common.map import Map
from game.common.node import Node

# Probably need to add some extra stuff
class Truck(GameObject):

    def __init__(self, node = None):
        super().__init__()
        self.object_type = ObjectType.truck
        self.current_node = node
        self.contract_list = []
        self.active_contract = None
        self.speed = 50

    def get_city_contracts(self):
        return self.contract_list

    def get_active_contract(self):
        return self.active_contract

    def get_current_speed(self):
        return self.speed

    def set_current_speed(self, speed):
        if speed < 1:
            speed = 1
        self.speed = speed
    
    def to_json(self):
        data = super().to_json()
        data['current_node'] = self.current_node
        data['speed'] = self.speed
        return data

    def from_json(self, data):
        super().from_json(data)
        node = Node()
        self.current_node = data['current_node']
        self.speed = data['speed']
