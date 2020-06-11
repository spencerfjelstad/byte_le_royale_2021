from game.config import *
from game.utils.helpers import write_json_file
from game.common.node import Node
from game.common.map import Map

def generate():
    print('Generating game map...')

    start = Node("Redwood Warehouse")
    a = Node("CityA")
    b = Node("CityB")
    c = Node("CityC")
    d = Node("CityD")
    start.Connect(a,"RA")
    start.Connect(b,"RB")
    start.Connect(c,"RC")
    start.Connect(d,"RD")
    a.Connect(b,"RE")
    d.Connect(c,"RF")

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    res = Map.getData()
    write_json_file(res, GAME_MAP_FILE)
