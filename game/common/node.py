from game.common.game_object import GameObject
from game.common.enums import ObjectType, LocationType

class Node(GameObject):

    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.node
        self.location_type = LocationType.none
        self.gas_station = None
        self.city_name = "City"
        self.connecting_cities = list()
        self.reward_modifier = None
        self.difficulty_modifier = None
    
    def to_json(self):
        data = super().to_json()
        data['location_type'] = self.location_type
        data['city_name'] = self.city_name
        data['connecting_cities'] = self.connecting_cities
        data['gas_station'] = self.gas_station
        data['reward_modifier'] = self.reward_modifier
        data['difficulty_modifier'] = self.difficulty_modifier
        return data

    def from_json(self, data):
        super().from_json(data),
        self.location_type = data['location_type']
        self.city_name = data['city_name']
        self.connecting_cities = data['connecting_cities']
        self.gas_station = data['gas_station']
        self.reward_modifier = data['reward_modifier']
        self.difficulty_modifier = data['difficulty_modifier']