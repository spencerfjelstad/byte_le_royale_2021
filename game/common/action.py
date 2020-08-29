from game.common.enums import *

from game.common.contract import Contract


class Action:
    def __init__(self):
        self.object_type = ObjectType.action
        self._chosen_action = None
        self.contract_index = None

    def set_action(self, action, contractIndex = None):
        self._chosen_action = action
        if action == ActionType.select_contract:
            self.contract_index = contractIndex
        else:
            self.contract_index = None
    
    def to_json(self):
        data = dict()

        data['object_type'] = self.object_type
        data['chosen_action'] = self._chosen_action

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._chosen_action = data['chosen_action']

    def __str__(self):
        outstring = ''
        outstring += f'Example Action: {self._chosen_action}\n'

        return outstring
