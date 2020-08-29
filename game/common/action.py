from game.common.enums import *


class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self._example_action = None
        self.__destination = None

    def set_action(self, action):
        self._example_action = action

    def get_destination(self):
        return self.__destination

    def set_destination (self, truck, destination):
        if not isinstance(destination, ObjectType.node):
            return
        if not isinstance(truck, ObjectType.truck):
            return
        self.current_location = truck.current_node
        for road in self.current_location.connections:
            if road.city_2 == destination.city_name:
                truck.current_node = destination
        self.__destination = destination

    def to_json(self):
        data = dict()

        data['object_type'] = self.object_type
        data['example_action'] = self._example_action

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._example_action = data['example_action']

    def __str__(self):
        outstring = ''
        outstring += f'Example Action: {self._example_action}\n'

        return outstring


