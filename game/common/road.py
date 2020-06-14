from game.common.game_object import GameObject
from game.common.enums import *
from game.common.map import Map
import json

class Road(GameObject):
    def __init__(self, name="road" ,city1=None, city2=None):
        super().__init__()
        self.object_type = ObjectType.node
        self.road_name = name
        self.road_type = RoadType.none
        self.city_1 = city1
        self.city_2 = city2
        Map.roads[self.road_name] = self
    
    def to_json(self):
        data = super().to_json()
        data['road_type'] = self.road_type
        data['road_name'] = self.road_name
        data['city_1'] = self.city_1
        data['city_2'] = self.city_2
        return data  
    
    def from_json(self,data):
        super().from_json(data)
        self.road_type = data['road_type']
        self.road_name = data['road_name']
        self.city_1 = data['city_1']
        self.city_2 = data['city_2']
        Map.roads.append(self)
    



