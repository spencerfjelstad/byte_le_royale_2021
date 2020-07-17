from game.common.game_object import GameObject
from game.common.enums import *
from game.common.map import Map
import random
import json


class Contract(GameObject):
    def __init__(self, name=None ,region=None, cities=None):
        super().__init__()
        self.object_type = ObjectType.contract
        
        # if no name is supplied it will generate a random one
        self.name = generateName() if not name else name
        # region is region enum
        self.region = region
        
        # cities is a list of strings representing the keys for the nodes within the graph
        self.cities = cities
    
    def to_json(self):
        data = super().to_json()
        data['name'] = self.name
        data['region'] = self.region
        data['cities'] = self.cities
        return data
    
    def from_json(self,data):
        super().from_json(data)
        self.name = data['name']
        self.region = data['region']
        self.cities = data['cities']

    # generates a random name, has no effect on gameplay other than lols
    def generateName(self):
        verb = ["Deliver ","Transport ","Drop off ","Ship "]
        quantity = ["a lot ","several ","one ","a few "]
        adjective = ["big ","small ","happy ","sad ","angry "]
        noun = ["lobsters","cd players", "power converers sourced from Tosche station", "Skinner Burgers"]
        if random.choice(noun) == "Skinner Burgers":
            return random.choice(verb) + random.choice(quantity) + "of" + random.choice(adjective) + "Skinner Burgers"
        return random.choice(verb) + random.choice(quantity) + "of " + random.choice(adjective) + random.choice(noun)
    
    def equals(self, contract):
        if self.name == contract.name and self.region == contract.region and self.cities == contract.cities:
            return True
        else:
            return False




