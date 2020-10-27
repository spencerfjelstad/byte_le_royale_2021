import uuid
from game.common.action import Action
from game.common.game_object import GameObject
from game.common.enums import *
from game.common.contract import Contract
from game.common.truck import Truck
from game.common.stats import GameStats


class Player(GameObject):
    # truck initialized with placeholder
    def __init__(self, code=None, team_name=None, action=None, contract=None, truck=Truck("HUB")):
        super().__init__()
        self.object_type = ObjectType.player
        self.functional = True
        self.error = None
        self.team_name = team_name
        self.code = code
        self.action = action
        self.truck = truck
        self.active_contract = contract
        self.time = GameStats.game_max_time
        self.money = GameStats.player_starting_money
        self.available_contracts = list()

    def to_json(self):
        data = super().to_json()

        data['functional'] = self.functional
        data['error'] = self.error
        data['team_name'] = self.team_name
        data['time'] = self.time
        data['action'] = self.action.to_json() if self.action is not None else dict()
        data['truck'] = self.truck.to_json()
        data['money'] = self.money
        data['active_contract'] = self.active_contract.to_json() if self.active_contract is not None else dict()
        return data

    def from_json(self, data):
        super().from_json(data)

        self.functional = data['functional']
        self.error = data['error']
        self.team_name = data['team_name']
        self.time = data['time']
        act = Action()
        self.action = act.from_json(data['action']) if data['action'] is not None else None
        truck = Truck()
        self.truck = truck.from_json(data['truck'])
        self.money = data['money']
        contract = Contract()
        self.active_contract = contract.from_json(data['active_contract'])

    def __str__(self):
        p = f"""ID: {self.id}
            Team name: {self.team_name}
            Action: {self.action}
            Contracts: {self.active_contract}
            Time: {self.time}
            Money: {self.money}
            """
        return p
