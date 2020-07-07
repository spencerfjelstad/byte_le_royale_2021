from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *
from game.common.map import Map

# Probably need to add some extra stuff
class Truck(GameObject):

    def __init__(self, node = None):
        super().__init__()
        self.object_type = ObjectType.truck
        self.current_node = node
        
    def to_json(self):
        data = super().to_json()
        data['current_node'] = self.current_node
        
        return data

    def from_json(self, data):
        super().from_json(data)
        self.current_node = data['current_node']
