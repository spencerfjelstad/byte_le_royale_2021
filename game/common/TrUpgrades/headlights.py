from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import *


class HeadLights(GameObject):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.headlights
        self.level = HeadlightLevel.level_zero
        self.highbeams = False

    def to_json(self):
        data = super().to_json()
        data['object_type'] = self.object_type
        data['level'] = self.level
        data['high_beams'] = self.highbeams
        return data

    def from_json(self, data):
        super().from_json(data)
        self.object_type = data['object_type']
        self.level = data['level']
        self.current_gas = data['high_beams']

    def __str__(self):
        p = f"""Headlight Level: {self.level}
             High beams on?: {self.max_gas}
            """
        return p
