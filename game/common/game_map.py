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
        if self.current_node.next_node is None:
            return False
        self.current_node = self.current_node.next_node
        return self.current_node

    # This method is almost entirely pointless
    def reset_current(self):
        self.current_node = self.head

    def length(self):
        i = 1
        curr = self.head
        if curr is None: return 0
        while curr.next_node is not None:
            curr = curr.next_node
            i += 1
        return i

    def to_list(self):
        curr_node = self.head
        node_list = []
        while curr_node is not None:
            node_list.append(curr_node)
            curr_node = curr_node.next_node
        return node_list

    def to_json(self):
        data = super().to_json()

        data['head'] = self.head.to_json()
        data['current_node'] = self.current_node.to_json()
        node_list = self.to_list()
        data['map'] = {node.city_name: node.to_json() for node in node_list}
        return data
    
    def from_json(self, data):
        super().from_json(data)

        iter_node = Node('iterative')
        for node in reversed(data['map'].values()):
            temp = iter_node.from_json(node)
            self.insert_node(temp)

        current_node = Node('current_node')
        current_node.from_json(data['current_node'])
        self.current_node = current_node
