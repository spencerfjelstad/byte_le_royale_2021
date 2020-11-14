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
    truck = 4
    contract = 5
    policeScanner = 6
    

class ActionType:
    none = 0
    select_route = 1
    buy_gas = 2
    upgrade = 3
    select_contract = 4

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
    rural = 1
    street = 2
    highway = 3

class NodeType:
    none = 0
    city = 1
    warehouse = 2
    road = 3

class EventType:
    city_upgrade = 0
    scanner_upgrade = 1

class ScannerLevel:
    level_zero = 0
    level_one = 1
    level_two = 2
    level_three = 3
