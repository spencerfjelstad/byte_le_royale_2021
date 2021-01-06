from game.common.TrUpgrades.baseUpgradeObject import BaseUpgradeObject
from game.common.stats import GameStats
from game.common.enums import ObjectType, TankLevel

class BaseBodyObject(BaseUpgradeObject):
    def __init__(self,objType, lev):
        super().__init__(objType, lev)
        self.current_gas = GameStats.truck_starting_gas 
        self.max_gas = GameStats.truck_starting_gas

    def to_json(self):
        data = super().to_json()
        data['current_gas'] = self.current_gas
        data['max_gas'] = self.max_gas
        return data

    def from_json(self, data):
        super().from_json(data)
        self.current_gas = data['current_gas']
        self.max_gas = data['max_gas']

    def __str__(self):
        p = f"""gas: {self.gas},
                Max Gas: {self.max_gas}
            """
        return p
