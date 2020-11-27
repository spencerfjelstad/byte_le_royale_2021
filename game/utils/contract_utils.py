from copy import deepcopy
import random

from game.utils.helpers import write_json_file
from game.common.action import Action
from game.controllers.controller import Controller

from game.common.node import Node
from game.common.map import Map
from game.common.contract import Contract
from game.common.truck import Truck
from game.common.enums import *

# Generate list of contracts, store for verification
def generate_contracts(client):
    city_list = []
    hub = None
    for city in Map.cities.values():
        if city.region == Map.getCityByName(client.truck.current_node.city_name).region:
            city_list.append(city)
    for city in Map.cities.values():
        if 'hub' in city.city_name.lower():
            hub = city

    # Placeholder contract generation
    contract_list = [
            Contract(None, Map.getCityByName(client.truck.current_node.city_name).region, [hub, random.choice(city_list)]),
            Contract(None, Map.getCityByName(client.truck.current_node.city_name).region, [hub, random.choice(city_list)]),
            Contract(None, Map.getCityByName(client.truck.current_node.city_name).region, [hub, random.choice(city_list)])]
    
    return contract_list
