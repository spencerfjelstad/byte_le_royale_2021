from game.common.TrUpgrades.baseUpgradeObject import BaseUpgradeObject
from game.common.enums import *
from game.common.stats import *


class PoliceScanner(BaseUpgradeObject):
    def __init__(self):
        super().__init__(ObjectType.policeScanner, ScannerLevel.level_zero)
        self.scanner_results = None

    def to_json(self):
        data = super().to_json()
        data['scanner_results'] = self.scanner_results
        return data

    def from_json(self, data):
        super().from_json(data)
        self.scanner_results = data['scanner_results']

    def __str__(self):
        p = super.__str__
        p += f"""Scanner Results: {self.scanner_results}"""
        return p
