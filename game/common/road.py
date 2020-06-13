from game.common.game_object import GameObject
from game.common.enums import ObjectType, RoadType

class Road(GameObject):

    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.road
        self.road_type = RoadType.none
        self.locations = list()
        self.distance = None
    
    def to_json(self):
        data = super().to_json()
        data['road_type'] = self.road_type
        data['locations'] = self.locations
        data['distance'] = self.distance
        return data

    def from_json(self, data):
        super().from_json(data)
        self.road_type = data['road_type']
        self.locations = data['locations']
        self.distance = data['distance']
        


