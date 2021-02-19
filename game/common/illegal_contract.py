import sys
import random
from game.common.contract import Contract
from game.common.stats import GameStats
from game.common.enums import *

class IllegalContract(Contract):
    # This is a really bad workaround to instantiate subclass from superclass
    def __init__(self, *args, level=None):
        contraband_levels = [ContrabandLevel.level_zero, ContrabandLevel.level_one, 
                ContrabandLevel.level_two]
        self.level = random.choice(contraband_levels) if level is None else level
        self.risk = GameStats.illegal_contract_stats['risk'][self.level]
        self.penalties = {'time_penalty': GameStats.illegal_contract_stats['time_penalty'], 
                'money_penalty': GameStats.illegal_contract_stats['money_penalty']}
        name = self.generate_name()
        mod = GameStats.illegal_contract_stats['reward_modifier'][self.level]
        if len(args) == 1:
            contract = args[0]
            super().__init__(name, contract.region, contract.game_map, contract.money_reward*mod, contract.renown_reward*mod, contract.deadline, contract.difficulty)
        else:
            super().__init__(name, args[1], args[2], args[3]*mod, args[3]*mod, args[4], args[5])

    def generate_name(self):
        verb = ["Smuggle ", "Bootleg ", "Run ", "Slip ", "Move "]
        quantity = ["a good amount of ", "a small amount of ", "some ", "a crate of "]
        adjective = ["pilfered ", "off the books ", "shady looking ", "sketchy "]
        noun = ["skooma", "moon sugar", "corellian spice", "bacta", "jet", "mentats", 
                "nanomachines", "kryptonite", "tribbles"]

        return random.choice(verb) + random.choice(quantity) + random.choice(adjective) + random.choice(noun)

    def to_json(self):
        data = super().to_json()
        data['level'] = self.level
        data['risk'] = self.risk
        data['penalties'] = self.penalties
        return data

    def from_json(self, data):
        super().from_json(data)
        self.level = data['level']
        self.risk = data['risk']
        self.penalties = data['penalties']
