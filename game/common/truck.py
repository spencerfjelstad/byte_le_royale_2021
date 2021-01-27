from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *
from game.common.node import Node
from game.common.TrUpgrades.BodyObjects.tank import Tank
from game.common.TrUpgrades.BodyObjects.headlights import HeadLights
from game.common.TrUpgrades.BodyObjects.sentry_gun import SentryGun
from game.common.TrUpgrades.gps import GPS
from game.common.TrUpgrades.rabbit_foot import RabbitFoot
from game.common.TrUpgrades.police_scanner import PoliceScanner
from game.common.stats import GameStats
from game.common.contract import Contract

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
        self.__speed = 50
        self.health = GameStats.truck_starting_health
        self.money = GameStats.player_starting_money
        self.renown = 0

    def get_city_contracts(self):
        return self.contract_list

    def get_active_contract(self):
        return self.active_contract

    def get_current_speed(self):
        return self.__speed

    def set_current_speed(self, speed):
        if speed < 1:
            speed = 1
        elif speed > GameStats.truck_maximum_speed:
            speed = GameStats.truck_maximum_speed
        self.__speed = speed

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
        node = self.current_node.to_json() if self.current_node is not None else None
        data['current_node'] = node
        data['contract_list'] = {contract.name: contract.to_json() for contract in self.contract_list}
        data['active_contract'] = self.active_contract.to_json() if self.active_contract is not None else None
        data['speed'] = self.__speed
        data['health'] = self.health
        data['money'] = self.money
        data['renown'] = self.renown
        data['event_type_bonus'] = self.event_type_bonus
        data['body'] = self.body.to_json()
        data['addons'] = self.addons.to_json()
        data['tires'] = self.tires
        return data

    def from_json(self, data):
        super().from_json(data)
        node = Node('temp')
        node.from_json(data['current_node'])
        self.current_node = node
        temp = Contract()
        for contract in data['contract_list'].values():
            self.contract_list.append(temp.from_json(contract))
        self.active_contract = temp.from_json(data['active_contract'])
        self.__speed = data['speed']
        self.health = data['health']
        self.money = data['money']
        self.renown = data['renown']
        self.event_type_bonus = data['event_type_bonus']
        if data['body']['object_type'] == ObjectType.headlights:
            headlights = HeadLights()
            headlights.from_json(data['body'])
            self.body = headlights
        elif data['body']['object_type'] == ObjectType.sentryGun:
            sentry_gun = SentryGun()
            sentry_gun.from_json(data['body'])
            self.body = sentry_gun
        elif data['body']['object_type'] == ObjectType.tank:
            tank = Tank()
            tank.from_json(data['body'])
            self.body = tank
        if data['addons']['object_type'] == ObjectType.policeScanner:
            police_scanner = PoliceScanner()
            police_scanner.from_json(data['addons'])
            self.addons = police_scanner
        elif data['addons']['object_type'] == ObjectType.rabbitFoot:
            rabbit_foot = RabbitFoot()
            rabbit_foot.from_json(data['addons'])
            self.addons = rabbit_foot
        elif data['addons']['object_type'] == ObjectType.GPS:
            gps = GPS()
            gps.from_json(data['addons'])
            self.addons = gps

        self.tires = data['tires']

    def __str__(self):
        contracts_string = []
        for contract in self.contract_list:
            contracts_string.append(str(contract))
        p = f"""Current Node: {self.current_node.city_name if self.current_node is not None else None}
            Contract List: {str(contracts_string)}
            Contract: {str(self.active_contract)}
            Gas: {self.body.current_gas}
            Max Gas: {self.body.max_gas}
            Speed: {self.__speed}
            Health: {self.health}
            Money: {self.money}
            Renown: {self.renown}
            Body: {self.body}
            """
        return p
