import random

from game.common.action import Action
from game.controllers.controller import Controller

from game.common.contract import Contract
from game.common.enums import *
from game.common.stats import GameStats
from game.common.region import *

from game.utils.create_game_map import create_game_map

# Generate list of contracts, store for verification
def generate_contracts(client):
    # Placeholder for now, will need balancing/changes in future
    region_list = [Region.grass_lands, Region.nord_dakotia, Region.mobave_desert,
            Region.mount_vroom, Region.lobslantis, Region.tropical_cop_land]

    easy_map = create_game_map(GameStats.contract_node_count['short'],
            GameStats.default_road_length-GameStats.road_length_maximum_deviation)

    medium_map = create_game_map(GameStats.contract_node_count['medium'],
            GameStats.default_road_length)

    hard_map = create_game_map(GameStats.contract_node_count['long'],
            GameStats.default_road_length-GameStats.road_length_maximum_deviation)

    # Currently region is random, not sure what to do with it
    easy_contract = Contract(None, random.choice(region_list), easy_map,
            GameStats.contract_rewards['easy'])
    medium_contract = Contract(None, random.choice(region_list), medium_map,
            GameStats.contract_rewards['medium'])
    hard_contract = Contract(None, random.choice(region_list), hard_map,
            GameStats.contract_rewards['hard'])

    contract_list = [easy_contract, medium_contract, hard_contract]

    return contract_list
