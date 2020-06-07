from game.common.node import Node
from game.common.enums import NodeType
from game.common.stats import GameStats

class Grass_Lands(Node):
    def __init__(self):
        super().__init__()
        self.node_type = NodeType.grass_lands
        self.reward_modifier = GameStats.node_reward_modifier[self.node_type]
        self.difficulty_modifier = GameStats.node_difficulty_modifier[self.node_type]

class Nord_Dakotia(Node):
    def __init__(self):
        super().__init__()
        self.node_type = NodeType.nord_dakotia
        self.reward_modifier = GameStats.node_reward_modifier[self.node_type]
        self.difficulty_modifier = GameStats.node_difficulty_modifier[self.node_type]

class Mobave_Desert(Node):
    def __init__(self):
        super().__init__()
        self.node_type = NodeType.mobave_desert
        self.reward_modifier = GameStats.node_reward_modifier[self.node_type]
        self.difficulty_modifier = GameStats.node_difficulty_modifier[self.node_type]

class Mount_Vroom(Node):
    def __init__(self):
        super().__init__()
        self.node_type = NodeType.mount_vroom
        self.reward_modifier = GameStats.node_reward_modifier[self.node_type]
        self.difficulty_modifier = GameStats.node_difficulty_modifier[self.node_type]

class Loblantis(Node):
    def __init__(self):
        super().__init__()
        self.node_type = NodeType.loblantis
        self.reward_modifier = GameStats.node_reward_modifier[self.node_type]
        self.difficulty_modifier = GameStats.node_difficulty_modifier[self.node_type]

class Tropical_Cop_Land(Node):
    def __init__(self):
        super().__init__()
        self.node_type = NodeType.tropical_cop_land
        self.reward_modifier = GameStats.node_reward_modifier[self.node_type]
        self.difficulty_modifier = GameStats.node_difficulty_modifier[self.node_type]

