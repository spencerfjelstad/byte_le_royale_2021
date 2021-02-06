from game.common.enums import *

from game.common.contract import Contract


class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self._chosen_action = None
        self.action_parameter = None
        self.__route = None

    def set_action(self, action, action_parameter = None):
        self._chosen_action = action
        self.action_parameter = action_parameter
    
    def get_route(self):
        return self.__route

    def set_route(self, route):
        if not isinstance(route, ObjectType.node):
            return
        self.__route = route

    def to_json(self):
        data = dict()

        data['object_type'] = self.object_type
        data['chosen_action'] = self._chosen_action
        data['destination'] = self.__route

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._chosen_action = data['chosen_action']
        self.__route = data['destination']

    def __str__(self):
        outstring = ''
        outstring += f'Example Action: {self._chosen_action}\n'

        return outstring
