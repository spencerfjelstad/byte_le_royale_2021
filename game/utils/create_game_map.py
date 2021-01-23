import random

from game.common.game_map import Game_Map
from game.common.node import Node
from game.common.road import Road
from game.common.stats import GameStats

def create_game_map(node_count, length):
    # Names
    meme_names = ["Tosche Station", "Toschetosche Station", "King's Landing",
    "Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch", "Fargo", 
    "goFar", "FarFar", "GoGo", "Nuketown", "de_Dust2", "Rapture", "Isengard",
    "Plastic Beach", "Los Santos", "Gotham city", "Mos Eisley", "Riften", "Whiterun",
    "Rorikstead"]

    normal_name_begins = ["Lazy","Big", "Dusty", "Plain", "Plank", "Spooky", 
    "Lucky", "Juicy", "Cowboy", "Barry", "Python", "Town", "SeaShaup", "Pearl", 
    "Susan", "Karen", "Chad", "Truck"]
    normal_name_ends = [" Basin", " City", "town", "ton", "ville", "bury", "field"]
    
    end_node = Node("end", [], None)
    g_map = Game_Map(end_node)
    
    av_road_length = length / node_count
    road_deviation = int(av_road_length * GameStats.road_length_variance)

    old_town_name = []
    for i in range(node_count, 0, -1):
        first_loop = True
        town_name = ""
        # On off chance we get a repeat name, do again
        while(first_loop or town_name in old_town_name):
            # If small chance, do meme name. Else, normal
            if(random.randint(1,10) == 1):
                town_name = meme_names[random.randint(0, len(meme_names) - 1)]
            else:
                town_name = normal_name_begins[random.randint(0, len(normal_name_begins) - 1)] + normal_name_ends[random.randint(0, len(normal_name_ends) - 1)]
            
            first_loop = False

        # Save valid town name to confirm no repeats
        old_town_name.append(town_name)
        

        roads = []
        for j in range(random.randint(2,3)):
            roads.append(Road("Route "+str(i)+"-"+str(j),
            random.randint(1, 6), av_road_length + random.randint(-1 * road_deviation, road_deviation)))
        temp_node = Node(town_name, roads, None)
        g_map.insert_node(temp_node)
    
    return g_map
