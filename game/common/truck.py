from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *
from game.common.node import Node
from game.common.TrUpgrades.police_scanner import PoliceScanner
from game.common.TrUpgrades.BodyObjects.tank import Tank
from game.common.stats import GameStats

# Probably need to add some extra stuff
class Truck(GameObject):

    def __init__(self, node = None):
        super().__init__()
        self.object_type = ObjectType.truck
        self.current_node = node
        self.contract_list = []
        self.active_contract = None
        self.body = Tank()
        self.addons = PoliceScanner()
        self.tires = TireType.tire_normal
        self.speed = 50
        self.health = GameStats.truck_starting_health
        

    def get_city_contracts(self):
        return self.contract_list

    def get_active_contract(self):
        return self.active_contract

    def get_current_speed(self):
        return self.speed

    def set_current_speed(self, speed):
        if speed < 1:
            speed = 1
        self.speed = speed
    
    event_type_bonus = {
        EventType.police: 0,
        EventType.animal_in_road: 0,
        EventType.bandits: 0,
        EventType.icy_road: 0,
        EventType.rock_slide: 0,
        EventType.traffic: 0
        }
   
    total_mountain_bonuses = event_type_bonus[EventType.police] + event_type_bonus[EventType.animal_in_road]\
        + event_type_bonus[EventType.icy_road] + event_type_bonus[EventType.rock_slide]
    total_forest_bonuses = event_type_bonus[EventType.police] + event_type_bonus[EventType.animal_in_road]\
        + event_type_bonus[EventType.icy_road] + event_type_bonus[EventType.rock_slide]
    total_tundra_bonuses = event_type_bonus[EventType.police]\
        + event_type_bonus[EventType.icy_road] + event_type_bonus[EventType.rock_slide]
    total_city_bonuses = event_type_bonus[EventType.police] + event_type_bonus[EventType.bandits]\
        + event_type_bonus[EventType.traffic]
    total_highway_bonuses = event_type_bonus[EventType.police] + event_type_bonus[EventType.traffic]
    total_interstate_bonuses = event_type_bonus[EventType.police] + event_type_bonus[EventType.traffic]

    def to_json(self):
        data = super().to_json()
        node = self.current_node
        data['current_node'] = node
        data['speed'] = self.speed
        data['health'] = self.health
        data['event_type_bonus'] = self.event_type_bonus
        data['body'] = self.body.to_json()
        data['addons'] = self.addons.to_json()
        data['tires'] = self.tires
        return data

    def from_json(self, data):
        super().from_json(data)
        self.current_node = data['current_node']
        self.speed = data['speed']
        self.event_type_bonus = data['event_type_bonus']
        self.body = data['body']
        self.addons = data['addons']
        self.tires = data['tires']
