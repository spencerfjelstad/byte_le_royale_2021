from game.common.enums import *

from game.common.contract import Contract
from game.common.player import Player


# Action modified for contracts to be private and generated during pre-tick
class Action:
    def __init__(self, contractList=None):
        self.object_type = ObjectType.action
        self._example_action = None
        self.__contract_list = contractList
        self._active_contract = None

    def set_action(self, action):
        if self._example_action != ActionType.select_contract:
            self._example_action = action

    def get_city_contracts(self):
        return self.__contract_list
    
    def get_active_contract(self):
        return self._active_contract
    
    # Action for easier access to updated value
    def select_contract(self, contractIndex):
        # Passed by index to prevent tampering
        if 0 < int(contractIndex) < len(self.__contract_list):
            self.__contract_list = self.__contract_list.pop(contractIndex)
            self._example_action = ActionType.select_contract
    
    def to_json(self):
        data = dict()

        data['object_type'] = self.object_type
        data['example_action'] = self._example_action
        data['contract_list'] = [c.to_json() for c in self.__contract_list]

        return data

    def from_json(self, data):
        self.object_type = data['object_type']
        self._example_action = data['example_action']
        self.__contract_list = data['contract_list']

    def __str__(self):
        outstring = ''
        outstring += f'Example Action: {self._example_action}\n'

        return outstring


