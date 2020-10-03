from game.controllers.controller import Controller
from game.common.enums import NodeType
class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.current_location = None

    def move(self, truck, road, speed):
        self.current_location = truck.current_node
        
        #if truck in on a road
        if type(self.current_location) is NodeType.road:
            current_road = self.current_location
            road_length = current_road.length

            current_distance = truck.current_distance
            distance = current_distance + truck.speed
            truck.current_distance = distance
            if truck.get_current_distance() > road_length or distance == road_length:
                truck.current_node = current_road.city_2
                truck.set_current_distance(0)

        #if truck is on city
        else:
            for route in self.current_location.connections:
                if route == road:
                    #put truck on chosen road and add speed to distance
                    truck.current_node = route
                    truck.set_current_distance(truck.speed)
        return road