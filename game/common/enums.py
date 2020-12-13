class DebugLevel:
    none = 0
    client = 1
    controller = 2
    engine = 3

class ObjectType:
    none = 0
    action = 1
    player = 2
    node = 3
    road = 4
    truck = 5
    contract = 6
    game_map = 7
    

class ActionType:
    none = 0
    select_route = 1
    buy_gas = 2
    upgrade = 3
    select_contract = 4
    choose_speed = 5

class Region:
    none = 0
    grass_lands = 1
    mount_vroom = 2
    mobave_desert = 3
    nord_dakotia = 4
    lobslantis = 5
    tropical_cop_land = 6

class RoadType:
    none = 0
    mountain_road = 1
    forest_road = 2
    tundra_road = 3
    highway = 4
    city_road = 5
    interstate = 6

class EventType:
    none = 0
    rock_slide = 1
    icy_road = 2
    animal_in_road = 3
    bandits = 4
    police = 5
    traffic = 6

