from game.common.TrUpgrades.BodyObjects.baseBodyObject import BaseBodyObject
from game.common.enums import *
from game.common.stats import *


class Tank(BaseBodyObject):
    def __init__(self):
        super().__init__(ObjectType.tank, TankLevel.level_zero)
        self.current_gas = GameStats.costs_and_effectiveness[ObjectType.tank]['effectiveness'][self.level] * GameStats.truck_starting_gas

    def to_json(self):
        data = super().to_json()
        data['current_gas'] = self.current_gas
        return data

    def from_json(self, data):
        super().from_json(data)
        self.current_gas = data['current_gas']

    def __str__(self):
        p = f"""Current Gas Level: {self.current_gas}
            Max Gas: {self.max_gas}
            """
        return p
