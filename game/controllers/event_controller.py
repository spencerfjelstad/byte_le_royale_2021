from game.common.stats import GameStats
from game.common.enums import EventType
import random

def trigger_event(road, player, truck):
    for i in range(len(GameStats.event_weights[road.road_type])-1):
        GameStats.event_weights[road.road_type][i] -= truck.event_type_bonus[GameStats.possible_event_types[road.road_type][i]]
        GameStats.event_weights[road.road_type][-1] += truck.event_type_bonus[GameStats.possible_event_types[road.road_type][i]]
    # Picks random event type from those possible on given road
    chosen_event_type = random.choices(GameStats.possible_event_types[road.road_type], weights=GameStats.event_weights[road.road_type], k=1)[0]
    
    # Deal damage based on event
    player.truck.health -= GameStats.event_type_damage[chosen_event_type]
    # Reduce remaining time based on event
    player.time -= GameStats.event_type_time[chosen_event_type]
    
def event_chance(road, player,truck):
    happens = random.choices([True, False], weights=GameStats.base_event_probability, k=1)[0]
    if happens:
        trigger_event(road,player, truck)

