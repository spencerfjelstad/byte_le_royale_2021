from game.common.TrUpgrades.baseUpgradeObject import BaseUpgradeObject
from game.common.enums import *
from game.common.stats import *


class RabbitFoot(BaseUpgradeObject):
    def __init__(self):
        super().__init__(ObjectType.rabbitFoot, RabbitFootLevel.level_zero)
        self.onTheMirror = False

    def to_json(self):
        data = super().to_json()
        data['onTheMirror'] = self.onTheMirror
        return data

    def from_json(self, data):
        super().from_json(data)
        self.scanner_results = data['onTheMirror']

    def __str__(self):
        p = f"""On the Mirror?: {self.onTheMirror}"""
        return p
