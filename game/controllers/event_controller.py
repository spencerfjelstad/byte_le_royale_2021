from game.common.stats import GameStats
from game.common.enums import EventType, ObjectType
from game.controllers.controller import Controller
import random
from game.controllers.controller import Controller


class EventController(Controller):

    def __init__(self):
        super().__init__()

    def trigger_event(self, road, player, truck):
        # Picks random event type from those possible on given road
        chosen_event_type = random.choices(list(GameStats.possible_event_types[road.road_type].keys()), weights=GameStats.possible_event_types[road.road_type].values(), k=1)[0]
        mods = self.negation(truck, chosen_event_type)

        # Deal damage based on event
        player.truck.health -= GameStats.event_type_damage[chosen_event_type] * (1 - mods['HealthMod'])
        # Reduce remaining time based on event
        player.time -= GameStats.event_type_time[chosen_event_type] * (1 - mods['DamageMod'])

    def event_chance(self, road, player, truck):
        #evaluate 25% chance
        happens = random.choices(
            [True, False], weights=GameStats.base_event_probability, k=1)[0]
        #event chance 25% -> 40% if truck going really fast
        if (truck.get_current_speed > 70):
            happens = random.choices([True, False], weights=[40,60], k=1)[0]
        if happens:
            self.trigger_event(road, player, truck)

    
    def calculateMod(self, obj, event):
        health = GameStats.costs_and_effectiveness[obj.object_type]['effectiveness'][obj.level]
        time = GameStats.costs_and_effectiveness[obj.object_type]['effectiveness'][obj.level]
        return (health, time)

    def calculateTireMod(self, obj, event):
        health = GameStats.costs_and_effectiveness[ObjectType.tires]['effectiveness'][obj]
        time =  GameStats.costs_and_effectiveness[ObjectType.tires]['effectiveness'][obj]
        return (health, time)

    def negation(self, truck, event):
        mods = {'HealthMod': 0, 'DamageMod': 0}
        objs = [truck.addons, truck.body]
        try:
            for obj in objs:
                if event in GameStats.negations[obj.object_type]:
                    potentialMod = self.calculateMod(obj, event)
                    mods['HealthMod'] = max(potentialMod[0], mods['HealthMod'])
                    mods['DamageMod'] = max(potentialMod[1], mods['DamageMod'])
            # The logic for tires is slightly different
            if event in GameStats.negations[truck.tires]:
                potentialMod = self.calculateTireMod(truck.tires, event)
                mods['HealthMod'] = max(potentialMod[0], mods['HealthMod'])
                mods['DamageMod'] = max(potentialMod[1], mods['DamageMod'])
            return mods
        except:
            return {'HealthMod': 0, 'DamageMod': 0}

    def handle_actions(self, client):
        return
