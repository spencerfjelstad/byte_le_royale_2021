from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *

class Node(GameObject):
    
    # Name is the key for this node in the graph it must be unique 
    def __init__(self, name, roads=[], next_node=None):
        super().__init__()
        self.object_type = ObjectType.node
        self.city_name = name
        self.roads = []
        self.next_node = next_node
    
    def to_json(self):
        data = super().to_json()
        data['city_name'] = self.city_name
        data['roads'] = self.roads
        data['next_node'] = self.next_node.to_json() if self.next_node is not None else None
        return data

    def from_json(self, data):
        super().from_json(data)
        self.city_name = data['city_name']
        self.roads = data['roads']
        node = Node('init')
        self.next_node = node.from_json(data['next_node']) if data['next_node']\
            is not None else None
