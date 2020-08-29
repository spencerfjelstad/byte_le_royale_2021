from game.common.node import Node
from game.common.stats import GameStats
from game.enums import *

class City(Node):
    def __init__(self):
        super().__init__(self, "AHHHH")
        self.nodeType = NodeType.City
        
        