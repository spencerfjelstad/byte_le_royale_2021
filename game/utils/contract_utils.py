import random

from game.common.action import Action
from game.controllers.controller import Controller

from game.common.contract import Contract
from game.common.enums import *
from game.common.stats import GameStats
from game.common.region import *

from game.utils.create_game_map import create_game_map

def check_contract_completion(client):
    if client.truck.active_contract is not None:
        # May want to impose a penalty for failed contract
        if client.truck.active_contract.deadline > client.time:
            client.truck.active_contract = None
            client.truck.map.current_node.next_node = None
        elif client.truck.map.current_node.next_node is None:
            client.truck.money += client.truck.active_contract.money_reward
            client.truck.renown += client.truck.active_contract.renown_reward
            client.truck.active_contract = None

# Generate list of contracts, store for verification
def generate_contracts(client):
    # Placeholder for now, will need balancing/changes in future
    region_list = [Region.grass_lands, Region.nord_dakotia, Region.mobave_desert,
            Region.mount_vroom, Region.lobslantis, Region.tropical_cop_land]
    easy_map = create_game_map(GameStats.contract_node_count['short'],
            GameStats.default_road_length * GameStats.contract_node_count['short'])
    medium_map = create_game_map(GameStats.contract_node_count['medium'],
            GameStats.default_road_length * GameStats.contract_node_count['medium'])
    hard_map = create_game_map(GameStats.contract_node_count['long'],
            GameStats.default_road_length * GameStats.contract_node_count['long'])

    easy_contract = Contract(None, random.choice(region_list), 
            GameStats.contract_rewards['money']['easy'], GameStats.contract_rewards['renown']['easy'],
            client.time-GameStats.contract_deadline['short'])
    medium_contract = Contract(None, random.choice(region_list), 
            GameStats.contract_rewards['money']['medium'], GameStats.contract_rewards['renown']['medium'],
            client.time-GameStats.contract_deadline['medium'])
    hard_contract = Contract(None, random.choice(region_list), 
            GameStats.contract_rewards['money']['hard'], GameStats.contract_rewards['renown']['hard'],
            client.time-GameStats.contract_deadline['long'])

    contract1 = {'contract': easy_contract, 'map': easy_map}
    contract2 = {'contract': medium_contract, 'map': medium_map}
    contract3 = {'contract': hard_contract, 'map': hard_map}

    contract_list = [contract1, contract2, contract3]

    return contract_list
