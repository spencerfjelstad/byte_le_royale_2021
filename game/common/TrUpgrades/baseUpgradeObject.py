from game.common.game_object import GameObject


class BaseUpgradeObject(GameObject):
    def __init__(self, objType, lev):
        super().__init__()
        self.object_type = objType
        self.level = lev

    def to_json(self):
        data = super().to_json()
        data['object_type'] = self.object_type
        data['level'] = self.level
        return data

    def from_json(self, data):
        super().from_json(data)
        self.object_type = data['object_type']
        self.level = data['level']

    def __str__(self):
        p = f"""Level: {self.level},
                Object Type: {self.object_type}
            """
        return p
