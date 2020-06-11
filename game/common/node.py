from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *
from game.common.map import Map

class Node(GameObject):

    def __init__(self, name="City"):
        super().__init__()
        self.object_type = ObjectType.node
        self.city_name = name
        self.location_type = LocationType.none
        self.connections = list()
        Map.cities.append(self)
    
    def to_json(self):
        data = super().to_json()
        data['location_type'] = self.location_type
        data['city_name'] = self.city_name
        data['connections'] = self.connections
        return data

    def from_json(self, data):
        super().from_json(data)
        self.location_type = data['location_type']
        self.city_name = data['city_name']
        self.connections = data['connections']

    def Connect(self,cityToConnect, roadName):
        road = Road(roadName,self,cityToConnect)
        self.connections.append(road.road_name)
        return road



    
    
   