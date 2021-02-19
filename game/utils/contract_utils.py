import random

from game.common.contract import Contract
from game.common.enums import *
from game.common.stats import GameStats
from game.common.region import *
from game.common.illegal_contract import IllegalContract

from game.utils.create_game_map import create_game_map

def check_contract_completion(client):
    state = ContractState.unchanged
    if client.truck.active_contract is not None:
        # May want to impose a penalty for failed contract
        if client.truck.active_contract.deadline > client.time:
            client.truck.active_contract = None
            state = ContractState.failed
        elif client.truck.active_contract.game_map.current_node.next_node is None:
            client.truck.money += client.truck.active_contract.money_reward
            client.truck.renown += client.truck.active_contract.renown_reward
            client.truck.active_contract = None
            state = ContractState.completed
    return state

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

    easy_contract = Contract(None, random.choice(region_list), easy_map,
            GameStats.contract_stats['money_reward']['easy'], 
            GameStats.contract_stats['renown_reward']['easy'],
            client.time-GameStats.contract_stats['node_count']['short'], 
            ContractDifficulty.easy)
    medium_contract = Contract(None, random.choice(region_list), medium_map,
            GameStats.contract_stats['money_reward']['medium'], 
            GameStats.contract_stats['renown_reward']['medium'],
            client.time-GameStats.contract_stats['deadline']['medium'], 
            ContractDifficulty.medium)
    hard_contract = Contract(None, random.choice(region_list), hard_map,
            GameStats.contract_stats['money_reward']['hard'], 
            GameStats.contract_stats['renown_reward']['hard'],
            client.time-GameStats.contract_stats['deadline']['long'],
            ContractDifficulty.hard)
    
    contract_list = [easy_contract, medium_contract, hard_contract]

    diff_list = ['easy', 'medium', 'hard']
    length_list = ['short', 'medium', 'long']
    for i in range(random.randint(1, 4)):
        rng = random.randint(ContractDifficulty.easy, ContractDifficulty.hard)
        game_map = create_game_map(GameStats.contract_stats['node_count'][length_list[rng]],
                GameStats.default_road_length * GameStats.contract_stats['node_count'][length_list[rng]])
        contract = Contract(None, random.choice(region_list), game_map,
            GameStats.contract_stats['money_reward'][diff_list[rng]], 
            GameStats.contract_stats['renown_reward'][diff_list[rng]],
            client.time-GameStats.contract_stats['deadline'][length_list[rng]], rng)
        contract_list.append(contract)

    rng = random.randint(1, 100)
    if rng <= 25:
        index = random.randrange(3, len(contract_list))
        illegal_contract = IllegalContract(contract_list[index])
        contract_list[index] = illegal_contract

    random.shuffle(contract_list)

    return contract_list
