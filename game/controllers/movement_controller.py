from game.controllers.controller import Controller
from game.common.enums import NodeType
from game.common import player
class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.current_location = None

    def move(self, truck, road):
        self.current_location = truck.current_node
        time_taken = 0
        for route in self.current_location.connections:
            if route == road:
                truck.current_node = route.city_2
                time_taken = road.length / truck.get_current_speed()
        player.time -= time_taken