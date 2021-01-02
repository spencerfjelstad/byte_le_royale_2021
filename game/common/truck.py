from game.common.game_object import GameObject
from game.common.enums import *
from game.common.road import *
from game.common.node import Node
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
        self.gas = GameStats.truck_starting_gas
        self.max_gas = GameStats.truck_starting_max_gas
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
        node = self.current_node.to_json() if self.current_node is not None else None
        data['current_node'] = node
        data['contract_list'] = {contract.name: contract.to_json() for contract in self.contract_list}
        data['active_contract'] = self.active_contract.to_json() if self.active_contract is not None else None
        data['gas'] = self.gas
        data['max_gas'] = self.max_gas
        data['speed'] = self.speed
        data['event_type_bonus'] = self.event_type_bonus
        data['health'] = self.health
        return data

    def from_json(self, data):
        super().from_json(data)
        node = Node('temp')
        self.current_node = node.from_json(data['current_node'])
        temp = Contract()
        for contract in data['contract_list'].values():
            self.contract_list.append(temp.from_json(contract))
        self.active_contract = temp.from_json(data['active_contract'])
        self.gas = data['gas']
        self.max_gas = data['max_gas']
        self.current_node = data['current_node']
        self.speed = data['speed']
        self.event_type_bonus = data['event_type_bonus']

    def __str__(self):
        contracts_string = []
        for contract in self.contract_list:
            contracts_string.append(str(contract))
        p = f"""Current Node: {self.current_node.city_name}
            Contract List: {str(contracts_string)}
            Contract: {str(self.active_contract)}
            Gas: {self.gas}
            Max Gas: {self.max_gas}
            Speed: {self.speed}
            Health: {self.health}
            """
        return p
