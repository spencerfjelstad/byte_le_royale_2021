from game.common.node import Node
from game.common.enums import Region
from game.common.stats import GameStats


class Grass_Lands(Node):
    def __init__(self):
        super().__init__()
        self.region = Region.grass_lands
        self.reward_modifier = GameStats.region_reward_modifier[self.region]
        self.difficulty_modifier = GameStats.node_difficulty_modifier[self.region]


class Nord_Dakotia(Node):
    def __init__(self):
        super().__init__()
        self.region = Region.nord_dakotia
        self.reward_modifier = GameStats.region_reward_modifier[self.region]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.region]


class Mobave_Desert(Node):
    def __init__(self):
        super().__init__()
        self.region = Region.mobave_desert
        self.reward_modifier = GameStats.region_reward_modifier[self.region]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.region]


class Mount_Vroom(Node):
    def __init__(self):
        super().__init__()
        self.region = Region.mount_vroom
        self.reward_modifier = GameStats.region_reward_modifier[self.region]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.region]


class Loblantis(Node):
    def __init__(self):
        super().__init__()
        self.region = Region.loblantis
        self.reward_modifier = GameStats.region_reward_modifier[self.region]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.region]


class Tropical_Cop_Land(Node):
    def __init__(self):
        super().__init__()
        self.region = Region.tropical_cop_land
        self.reward_modifier = GameStats.region_reward_modifier[self.region]
        self.difficulty_modifier = GameStats.region_difficulty_modifier[self.region]
