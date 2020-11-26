from game.common.game_object import GameObject
from game.common.enums import *
from game.common.map import Map
from game.common.stats import GameStats
import json

class Road(GameObject):
    # name is the key for this edge, it must always be unique
    def __init__(self, name, road_type=RoadType.none, length=GameStats.default_road_length):
        super().__init__()
        self.object_type = ObjectType.road
        self.road_name = name
        self.road_type = road_type
        self.length = length

    
    def to_json(self):
        data = super().to_json()
        data['road_type'] = self.road_type
        data['road_name'] = self.road_name
        data['length'] = self.length
        return data  
    
    def from_json(self,data):
        super().from_json(data)
        self.road_type = data['road_type']
        self.road_name = data['road_name']
        self.length = data['length']
    



