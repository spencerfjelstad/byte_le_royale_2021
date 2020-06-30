from game.common.action import Action
from game.common.enums import ActionType, ObjectType, LocationType

class SelectRoute(Action):
    def __init__(self, truck=None, destination=None):
        super().__init__()
        self.action_type = SelectRoute
        self.starting_location = truck.current_location
        self.destination = destination

    def to_json(self):
        data = super.to_json()
        data['starting_location'] = self.starting_location
        data['destination'] = self.destination

    def from_json(self, data):
        data = super.from_json()
        self.starting_location = data['starting_location']
        self.destination_list = data['destination_list']