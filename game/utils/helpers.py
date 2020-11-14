from game.common import enums
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

def addTogetherDictValues(dict):
    sum = 0
    for val in dict:
        sum += dict[val]
    return sum


def getNextLevel(enumType, curLevel):
    nextWord = { 0 : 'one' , 1 : 'two' , 2 : 'two',  3 : 'four' , 5 : 'six' , 6 : 'seven', 7 : 'eight'}
    word = nextWord[curLevel]
    for key in enumType.__dict__.keys():
        if(word in key.split('_', -1)):
            return key
    breakpoint()
    raise Exception("Cannot find a valid next level")


    

