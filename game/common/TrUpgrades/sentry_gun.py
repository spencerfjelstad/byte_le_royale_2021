from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import *


class SentryGun(GameObject):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.sentryGun
        self.level = SentryGunLevel.level_zero
        self.MissleLauncher = False

    def to_json(self):
        data = super().to_json()
        data['object_type'] = self.object_type
        data['level'] = self.level
        data['missleLauncher'] = self.MissleLauncher
        return data

    def from_json(self, data):
        super().from_json(data)
        self.object_type = data['object_type']
        self.level = data['level']
        self.current_gas = data['missleLauncher']

    def __str__(self):
        p = f"""Headlight Level: {self.level}
             missle Launcher on?: {self.max_gas}
            """
        return p
