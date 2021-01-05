from game.common.TrUpgrades.baseUpgradeObject import BaseUpgradeObject
from game.common.enums import *
from game.common.stats import *


class GPS(BaseUpgradeObject):
    def __init__(self):
        super().__init__(ObjectType.GPS, GPSLevel.level_zero)

    def to_json(self):
        data = super().to_json()
        return data

    def from_json(self, data):
        super().from_json(data)

    def __str__(self):
        p = super.__str__
        return p
