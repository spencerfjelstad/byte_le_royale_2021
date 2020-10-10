from game.common.node import Node
from game.common.enums import Region
from game.common.stats import GameStats


class Grass_Lands(Node):
    def __init__(self):
        super().__init__()
        self.location_type = Region.grass_lands
        self.reward_modifier = GameStats.region_reward_modifier[self.location_type]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.location_type]


class Nord_Dakotia(Node):
    def __init__(self):
        super().__init__()
        self.location_type = Region.nord_dakotia
        self.reward_modifier = GameStats.region_reward_modifier[self.location_type]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.location_type]


class Mobave_Desert(Node):
    def __init__(self):
        super().__init__()
        self.location_type = Region.mobave_desert
        self.reward_modifier = GameStats.region_reward_modifier[self.location_type]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.location_type]


class Mount_Vroom(Node):
    def __init__(self):
        super().__init__()
        self.location_type = Region.mount_vroom
        self.reward_modifier = GameStats.region_reward_modifier[self.location_type]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.location_type]


class Loblantis(Node):
    def __init__(self):
        super().__init__()
        self.location_type = Region.lobslantis
        self.reward_modifier = GameStats.region_reward_modifier[self.location_type]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.location_type]


class Tropical_Cop_Land(Node):
    def __init__(self):
        super().__init__()
        self.location_type = Region.tropical_cop_land
        self.reward_modifier = GameStats.region_reward_modifier[self.location_type]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.location_type]
