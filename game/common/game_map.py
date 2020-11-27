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
        self.current_node = self.head
        # I sort of want to make current a list of both
        # the node and the index of the node, but I don't
        # know if that's needed.

    def insert_node(self, node):
        node.next_node = self.head
        self.head = node
        self.current_node = node
    
    # This method just makes parsing easier
    def get_next_node(self):
        if self.current_node.next_node == None:
            return False
        self.current_node = self.current_node.next_node
        return self.current_node

    # This method is almost entirely pointless
    def reset_current(self):
        self.current_node = self.head

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
