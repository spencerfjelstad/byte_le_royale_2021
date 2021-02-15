import random

from game.common.contract import Contract
from game.common.enums import *
from game.common.stats import GameStats
from game.common.region import *
from game.common.illegal_contract import IllegalContract

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
    easy_map = create_game_map(GameStats.contract_stats['node_count']['short'],
            GameStats.default_road_length * GameStats.contract_stats['node_count']['short'])
    medium_map = create_game_map(GameStats.contract_stats['node_count']['medium'],
            GameStats.default_road_length * GameStats.contract_stats['node_count']['medium'])
    hard_map = create_game_map(GameStats.contract_stats['node_count']['long'],
            GameStats.default_road_length * GameStats.contract_stats['node_count']['long'])

    easy_contract = Contract(None, random.choice(region_list), 
            GameStats.contract_stats['money_reward']['easy'], 
            GameStats.contract_stats['renown_reward']['easy'],
            client.time-GameStats.contract_stats['node_count']['short'], 
            ContractDifficulty.easy)
    medium_contract = Contract(None, random.choice(region_list),
            GameStats.contract_stats['money_reward']['medium'], 
            GameStats.contract_stats['renown_reward']['medium'],
            client.time-GameStats.contract_stats['deadline']['medium'], 
            ContractDifficulty.medium)
    hard_contract = Contract(None, random.choice(region_list),
            GameStats.contract_stats['money_reward']['hard'], 
            GameStats.contract_stats['renown_reward']['hard'],
            client.time-GameStats.contract_stats['deadline']['long'],
            ContractDifficulty.hard)

    contract1 = {'contract': easy_contract, 'map': easy_map}
    contract2 = {'contract': medium_contract, 'map': medium_map}
    contract3 = {'contract': hard_contract, 'map': hard_map}
    
    contract_list = [contract1, contract2, contract3]

    diff_list = ['easy', 'medium', 'hard']
    length_list = ['short', 'medium', 'long']
    temp_list = []
    for i in range(random.randint(1, 4)):
        rng = random.randint(ContractDifficulty.easy, ContractDifficulty.hard)
        contract = Contract(None, random.choice(region_list),
            GameStats.contract_stats['money_reward'][diff_list[rng]], 
            GameStats.contract_stats['renown_reward'][diff_list[rng]],
            client.time-GameStats.contract_stats['deadline'][length_list[rng]], rng)
        game_map = create_game_map(GameStats.contract_stats['node_count'][length_list[rng]],
                GameStats.default_road_length * GameStats.contract_stats['node_count'][length_list[rng]])
        contract_pair = {'contract': contract, 'map': game_map}
        temp_list.append(contract_pair)

    rng = random.randint(1, 100)
    if rng <= 25:
        index = random.randrange(0, len(temp_list))
        illegal_contract = IllegalContract(temp_list[index]['contract'])
        temp_list[index]['contract'] = illegal_contract

    contract_list.extend(temp_list)
    random.shuffle(contract_list)

    return contract_list
