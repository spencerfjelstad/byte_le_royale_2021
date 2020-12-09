from game.config import *
from game.utils.helpers import write_json_file
from game.common.node import Node
import random
import sys

def generate():
    print('Generating game map...')

    # Verify logs location exists
    if not os.path.exists(GAME_MAP_DIR):
        os.mkdir(GAME_MAP_DIR)

    res = {}

    # Generates random seeds for turns
    for i in range(1, MAX_TICKS + 1):
        res[i] = dict()
        res[i]["seed"] = random.randint(1,sys.maxsize)
    
    write_json_file(res, GAME_MAP_FILE)
