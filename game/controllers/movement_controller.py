from game.controllers.controller import Controller
from game.common.enums import NodeType
from game.common.player import Player
class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.current_location = None

    def move(self, player, road):
        self.current_location = player.truck.current_node
        time_taken = 0
        for route in self.current_location.connections:
            if route is road:
                player.truck.current_node = route.city_2
                time_taken = road.length / player.truck.get_current_speed()
        player.time -= time_taken
