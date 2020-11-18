from game.common.game_object import GameObject
from game.common.enums import *
from game.common.node import Node

class GameMap(GameObject):

    # This will be a singly-linked list
    # Sort-of. Kinda.
    def __init__(self, node=None):
        super().__init__()
        self.object_type = ObjectType.game_map
        self.head = node

