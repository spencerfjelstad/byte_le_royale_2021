from game.config import *
from game.utils.helpers import write_json_file
from game.common.node import Node
from game.common.map import Map
from game.common.enums import Region

# This method generates a map
# STATIC METHOD BAAADDDD
def generateMap():
    start_node = Node("HUB")
    start_node.region = Region.nord_dakotia
#    a = Node("CityA")
#    b = Node("CityB")
#    c = Node("CityC")
#    d = Node("CityD")
    
#    start.Connect(a,"RA")
#    start.Connect(b,"RB")
#    start.Connect(c,"RC")
#    start.Connect(d,"RD")
#    a.Connect(b,"RE")
#    d.Connect(c,"RF")
