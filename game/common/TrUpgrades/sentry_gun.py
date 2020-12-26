from game.common.TrUpgrades.baseUpgradeObject import BaseUpgradeObject
from game.common.enums import *
from game.common.stats import *


class SentryGun(BaseUpgradeObject):
    def __init__(self):
        super().__init__(ObjectType.sentryGun,SentryGunLevel.level_zero)
        self.MissileLauncher = False

    def to_json(self):
        data = super().to_json()
        data['missileLauncher'] = self.MissileLauncher
        return data

    def from_json(self, data):
        super().from_json(data)
        self.MissileLauncher = data['missileLauncher']

    def __str__(self):
        p = super.__str__
        p += f"""missle Launcher on?: {self.missileLauncher}"""
        return p
