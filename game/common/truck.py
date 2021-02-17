from game.common.TrUpgrades.baseUpgradeObject import BaseUpgradeObject
from game.common.TrUpgrades.BodyObjects.baseBodyObject import BaseBodyObject
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

    def __init__(self, game_map = None):
        super().__init__()
        self.object_type = ObjectType.truck
        self.map = game_map
        self.contract_list = []
        self.active_contract = None
        self.body = BaseBodyObject(0,0)
        self.addons = BaseUpgradeObject(0,0)
        self.tires = TireType.tire_normal
        self.speed = 50
        self.health = GameStats.truck_starting_health
        self.money = GameStats.player_starting_money
        self.renown = 0

    def get_city_contracts(self):
        return self.contract_list

    def get_active_contract(self):
        return self.active_contract

    def get_current_speed(self):
        return self.speed

    def set_current_speed(self, speed):
        if speed < 1:
            speed = 1
        elif speed > GameStats.truck_maximum_speed:
            speed = GameStats.truck_maximum_speed
        self.speed = speed

    def to_json(self):
        data = super().to_json()
        #data['map'] = self.map.to_json() if self.map is not None else None
        temp_list = [] 
        for i in self.contract_list:
            temp_dict = {'contract': i['contract'].to_json(), 'map': i['map'].to_json()}
            temp_list.append(temp_dict)
        #data['contract_list'] = temp_list
        data['active_contract'] = self.active_contract.to_json() if self.active_contract is not None else None
        data['speed'] = self.speed
        data['health'] = self.health
        data['money'] = self.money
        data['renown'] = self.renown
        data['body'] = self.body.to_json()
        data['addons'] = self.addons.to_json()
        data['tires'] = self.tires
        return data

    def from_json(self, data):
        super().from_json(data)
        json_map = Game_Map()
        json_map.from_json(data['map'])
        self.game_map = json_map

        temp_contract = Contract()
        temp_map = Game_Map()
        temp_list = []
        for i in data['contract_list']:
            temp_contract.from_json(i['contract']) 
            temp_map.from_json(i['map'])
            temp_dict = {'contract': temp_contract, 'map': temp_map}
            temp_list.append(temp_dict)
        self.contract_list = temp_list
        self.active_contract = temp.from_json(data['active_contract'])
        self.speed = data['speed']
        self.health = data['health']
        self.money = data['money']
        self.renown = data['renown']
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
        p = f"""Contract List: {str(contracts_string)}
            Contract: {str(self.active_contract)}
            Gas: {self.body.current_gas}
            Max Gas: {self.body.max_gas}
            Speed: {self.speed}
            Health: {self.health}
            Money: {self.money}
            Renown: {self.renown}
            Body: {self.body}
            """
        return p
