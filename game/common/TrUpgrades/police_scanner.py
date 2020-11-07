from game.common.game_object import GameObject
from game.common.enums import *
from game.common.stats import *
from game.utils.helpers import enum_to_string


class PoliceScanner(GameObject):
    def __init__(self):
        super().__init__()
        self.object_type = ObjectType.police_scanner
        self.level = scanner.level_zero
        self.scanner_results = None

    def to_json(self):
        data = super().to_json()

        data['object_type'] = self.object_type
        data['level'] = self.level
        data['scanner_results'] = self.sensor_results
        return data

    def from_json(self, data):
        super().from_json(data)
        self.object_type = data['object_type']
        self.level = data['level']
        self.scanner_results = data['scanner_results']

    def __str__(self):
        p = f"""Scanner Level: {self.level}
            Scanner Results: {self.scanner_results}
            """
        return p
