from game.common.game_object import GameObject
from game.common.enums import ObjectType, NodeType

class Node(GameObject):

    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.node
        self.node_type = NodeType.none
        self.gas_station = None
        self.city_name = "City"
        self.connecting_cities = dict()
    
    def to_json(self):
        data = super().to_json()
        data['node_type'] = self.node_type
        data['city_name'] = self.city_name
        data['connecting_cities'] = self.connecting_cities
        data['gas_station'] = self.gas_station
        return data

    def from_json(self, data):
        super.from_json(data)
        self.node_type = data['node_type']
        self.city_name = data['city_name']
        self.connecting_cities = data['connecting_cities']
        self.gas_station = data['gas_station']