from game.controllers.singleton_controller import Controller

class MovementController(Controller):

    def __init__(self):
        super().__init__()
        self.current_location = None

    def calculate_time_taken(self, distance, speed):
        return distance / speed


    def move(self, truck, destination, world_data):
        self.current_location = truck.current_node
        for road in self.current_location.connections:
            if road.city_2 == destination.city_name or road.city_1 == destination.city_name:
                truck.current_node = destination
                data["time_taken"] += self.calculate_time_taken(road.distance, truck.speed)    
        return destination