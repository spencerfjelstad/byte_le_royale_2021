from game.common.TrUpgrades.baseUpgradeObject import baseUpgradeObject
from game.common.enums import *
from game.common.stats import *


class HeadLights(baseUpgradeObject):
    def __init__(self):
        super().__init__(ObjectType.headlights, HeadlightLevel.level_zero)
        self.highbeams = False

    def to_json(self):
        data = super().to_json()
        data['high_beams'] = self.highbeams
        return data

    def from_json(self, data):
        super().from_json(data)
        self.current_gas = data['high_beams']

    def __str__(self):
        p = super.__str__
        p += f"""High beams on?: {self.max_gas}"""
        return p
