from game.common.game_object import GameObject
from game.common.enums import *
from game.common.node import Node

class Game_Map(GameObject):

    # This will be a singly-linked list
    # Sort-of. Kinda. Python is weird about it
    def __init__(self, node=None):
        super().__init__()
        self.object_type = ObjectType.game_map
        self.head = node

    def insert_node(self, node):
        node.next_node = self.head
        self.head = node
    
    def length(self):
        i = 1
        curr = self.head
        if curr == None: return 0
        while curr.next_node != None:
            curr = curr.next_node
            i += 1
        return i

    def to_json(self):
        return
    
    def from_json(self):
        return
