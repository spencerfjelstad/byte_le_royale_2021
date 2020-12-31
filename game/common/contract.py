from game.common.game_object import GameObject
from game.common.enums import *
import random
import json
from game.common.stats import GameStats


class Contract(GameObject):
    def __init__(self, name=None, region=None, game_map=None, reward=None):
        super().__init__()
        self.object_type = ObjectType.contract
        
        # if no name is supplied it will generate a random one
        self.name = self.generateName() if not name else name
        # region is region enum
        self.region = region
        
        # Contract holds the game map
        self.game_map = game_map
        self.reward = reward * GameStats.region_reward_modifier[region]
    
    def to_json(self):
        data = super().to_json()
        data['name'] = self.name
        data['region'] = self.region
        data['game_map'] = self.game_map.to_json()
        data['reward'] = self.reward
        return data
    
    def from_json(self,data):
        super().from_json(data)
        self.name = data['name']
        self.region = data['region']
        self.game_map = data['game_map']
        self.reward = data['reward']

    # generates a random name, has no effect on gameplay other than lols
    def generateName(self):
        verb = ["Deliver ", "Transport ", "Drop off ", "Ship "]
        quantity = ["a lot ", "several ", "one ", "a few "]
        adjective = ["big ", "small ", "happy ", "sad ", "angry "]
        noun = ["lobsters", "cd players", "power converters sourced from Tosche station", "Patented Skinner Burgers"]
        # Literally making code worse for a joke
        index = random.randrange(len(noun))
        if index == 3:
            return random.choice(verb) + random.choice(quantity) + "of " + noun[index]
        else:
            return random.choice(verb) + random.choice(quantity) + "of " + random.choice(adjective) + noun[index]
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name and self.region == other.region and self.cities == other.cities

    def __str__(self):
        p = f"""Name: {self.name}
            Region: {self.region}
            Reward: {self.reward}
            Map: {str(self.game_map.to_list())}
            """
        return p
