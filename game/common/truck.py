from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *
from game.common.map import Map
from game.common.node import Node
from game.common.stats import GameStats

# Probably need to add some extra stuff
class Truck(GameObject):

    def __init__(self, node = None):
        super().__init__()
        self.object_type = ObjectType.truck
        self.current_node = node
        self.contract_list = []
        self.active_contract = None
        self.gas = GameStats.truck_starting_gas
        self.max_gas = GameStats.truck_starting_max_gas

    def get_city_contracts(self):
        return self.contract_list

    def get_active_contract(self):
        return self.active_contract

    def to_json(self):
        data = super().to_json()
        data['current_node'] = self.current_node
        data['gas'] = self.gas
        data['max_gas'] = self.max_gas
        return data

    def from_json(self, data):
        super().from_json(data)
        node = Node()
        self.current_node = node.from_json(data['current_node'])
        self.gas = data['gas']
        self.max_gas = data['max_gas']
