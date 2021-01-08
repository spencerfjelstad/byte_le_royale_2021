import random

from game.common.game_map import Game_Map
from game.common.node import Node
from game.common.road import Road
from game.common.stats import GameStats

def create_game_map(node_count, length):
    end_node = Node("end", [], None)
    g_map = Game_Map(end_node)
    
    av_road_length = length / node_count
    road_deviation = int(av_road_length * GameStats.road_length_variance)

    for i in range(node_count, 0, -1):
        roads = []
        for j in range(random.randint(2,3)):
            roads.append(Road("Route "+str(i)+"-"+str(j),
            random.randint(0, 6), av_road_length + random.randint(-1 * road_deviation, road_deviation)))
        temp_node = Node(str(i), roads, None)
        g_map.insert_node(temp_node)
    
    return g_map
