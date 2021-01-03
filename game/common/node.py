from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *

class Node(GameObject):
    
    def __init__(self, name, roads=[], next_node=None):
        super().__init__()
        self.object_type = ObjectType.node
        self.city_name = name
        self.roads = []
        self.next_node = next_node
    
    def to_json(self):
        data = super().to_json()
        data['city_name'] = self.city_name
        data['roads'] = {road.road_name: road.to_json() for road in self.roads}
        data['next_node'] = self.next_node.to_json() if self.next_node is not None else None
        return data

    def from_json(self, data):
        super().from_json(data)
        self.city_name = data['city_name']
        temp = Road('temp')
        for road in data['roads'].values():
            self.roads.append(temp.from_json(road))

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
