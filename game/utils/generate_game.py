from game.config import *
from game.utils.helpers import write_json_file
from game.common.node import Node
from game.common.map import Map
from game.utils.CreateMap import *

def generate():
    print('Generating game map...')

    generateMap()
    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    # Write game map to file
    res = Map.getData()
    write_json_file(res, GAME_MAP_FILE)
