from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import *


class Tank(GameObject):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.tank
        self.level = TankLevel.level_zero
        self.current_gas = GameStats.gas_max_level[self.level]

    def to_json(self):
        data = super().to_json()
        data['object_type'] = self.object_type
        data['level'] = self.level
        data['current_gas'] = self.current_gas
        return data

    def from_json(self, data):
        super().from_json(data)
        self.object_type = data['object_type']
        self.level = data['level']
        self.current_gas = data['current_gas']

    def __str__(self):
        p = f"""Gas Tank Level: {self.level}
            Current Gas Level: {self.max_gas}
            Max Gas: {self.max_gas}
            """
        return p
