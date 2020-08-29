from game.common.enums import ActionType
from game.common.stats import GameStats
from game.controllers.controller import Controller
from game.utils.helpers import determine_if_connected
from game.common.truck import Truck
from game.controllers.master_controller import subtract_time
from game.common.road import Road

class ActionController(Controller):

    def update_destination(self, dest):
        self.Destination = dest


    def handle_movement(self, client):
        #Returns the road that connects the two roads, or None if not connected
        road = determine_if_connected(client.current_node, self.Destination)
        if (!road and self.Destination is not None):
            client.current_node = self.Destination
            subtract_time(road.)
            
            

            # Determine if the truck can still move this turn?
            # Get the current node the truck is at
            # Determine if the node the truck wants to move to is connected to the node the truck is at
            # Move the truck.
            #
        