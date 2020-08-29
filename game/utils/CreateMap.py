from game.config import *
from game.utils.helpers import write_json_file
from game.common.node import Node
from game.common.map import Map

# This method generates a map
# STATIC METHOD BAAADDDD
def generateMap():
    start = Node("HUB")
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