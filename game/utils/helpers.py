import json
from game.common.node import Node

def write_json_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def determine_if_connected(cityOne, cityTwo):
    for road in cityOne.connections:
        if(road.city1 is cityTwo or road.city2 is cityTwo):
            return road
    return None
    

