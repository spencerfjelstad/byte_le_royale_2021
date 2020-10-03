from game.common.game_object import GameObject
from game.common.enums import *
from game.common.map import Map
import json

class Road(GameObject):
    # name is the key for this edge, it must always be unique
    # city1 and city2 are strings representing the keys of the connected cities
    def __init__(self, name ,city1=None, city2=None, length=100):
        super().__init__()
        self.object_type = ObjectType.node
        self.road_name = name
        self.road_type = RoadType.none
        self.city_1 = city1
        self.city_2 = city2
        self.length = length
        # upon finishing up it adds itself to the graph. could add some errors if the key isn't unique
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
        Map.roads[self.road_name] = self
    



