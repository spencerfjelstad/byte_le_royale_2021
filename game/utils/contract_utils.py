from copy import deepcopy
import random

from game.utils.helpers import write_json_file
from game.common.action import Action
from game.controllers.controller import Controller

from game.common.node import Node
from game.common.game_map import Game_Map
from game.common.contract import Contract
from game.common.truck import Truck
from game.common.enums import *
from game.common.stats import GameStats
from game.common.region import *

from game.utils.create_game_map import create_game_map

# Generate list of contracts, store for verification
def generate_contracts(client):
    # Placeholder for now, will need balancing/changes in future
    region_list = [Region.grass_lands, Region.nord_dakotia, Region.mobave_desert, 
            Region.mount_vroom, Region.lobslantis, Region.tropical_cop_land]

    easy_map = create_game_map(ContractNodeCount.short,
            GameStats.default_road_length-GameStats.road_length_maximum_deviation)

    medium_map = create_game_map(ContractNodeCount.medium, GameStats.default_road_length)

    hard_map = create_game_map(ContractNodeCount.hard,
            GameStats.default_road_length-GameStats.road_length_maximum_deviation)

    # Currently region is random, not sure what to do with it
    easy_contract = Contract(None, random.choice(region_list), easy_map, ContractRewards.easy)
    medium_contract = Contract(None, random.choice(region_list), medium_map, ContractRewards.medium)
    hard_contract = Contract(None, random.choice(region_list), medium_map, ContractRewards.hard)

    contract_list = [easy_contract, medium_contract, hard_contract]

    return contract_list
