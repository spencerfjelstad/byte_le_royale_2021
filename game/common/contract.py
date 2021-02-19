from game.common.game_object import GameObject
from game.common.enums import *
import random
import json, math
from game.common.stats import GameStats


class Contract(GameObject):
    def __init__(self, name=None, region=None, game_map=None, money_reward=None,
            renown_reward=None, deadline=None, difficulty=None):
        super().__init__()
        self.object_type = ObjectType.contract
        # if no name is supplied it will generate a random one
        self.name = self.generateName() if not name else name
        # region is region enum
        self.region = region
        self.game_map = game_map
        self.money_reward = (int(money_reward * GameStats.region_money_reward_modifier[region])
                if money_reward is not None and region is not None else 0)
        self.renown_reward = (int(math.ceil(renown_reward * GameStats.region_renown_reward_modifier[region]))
                if renown_reward is not None and region is not None else 0)
        self.deadline = deadline
        self.difficulty = difficulty
    
    def to_json(self):
        data = super().to_json()
        data['name'] = self.name
        data['region'] = self.region
        data['game_map'] = self.game_map.to_json()
        data['money_reward'] = self.money_reward
        data['renown_reward'] = self.renown_reward
        data['deadline'] = self.deadline
        data['difficulty'] = self.difficulty
        return data
    
    def from_json(self,data):
        super().from_json(data)
        self.name = data['name']
        self.region = data['region']
        json_map = Game_Map()
        json_map.from_json(data['game_map'])
        self.game_map = json_map
        self.money_reward = data['money_reward']
        self.renown_reward = data['renown_reward']
        self.deadline = data['deadline']
        self.difficulty = data['difficulty']

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

    def __str__(self):
        p = f"""Name: {self.name}
            Region: {self.region}
            Money Reward: {self.money_reward}
            Renown Reward: {self.renown_reward}
            Deadline: {self.deadline}
            """
        return p

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.name == other.name and self.region == other.region
                and self.game_map == other.game_map and self.money_reward == other.money_reward 
                and self.renown_reward == other.renown_reward and self.deadline == other.deadline 
                and self.difficulty == other.difficulty)
