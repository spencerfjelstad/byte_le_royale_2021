from game.common.stats import GameStats
from game.common.enums import EventType
import random

def trigger_event(road, player):
    # Picks random event type from those possible on given road
    chosen_event_type = random.choices(GameStats.possible_event_types[road.road_type], weights=GameStats.event_weights[road.road_type], k=1)[0]
    
    # Deal damage based on event
    player.truck.health -= GameStats.event_type_damage[chosen_event_type]
    # Reduce remaining time based on event
    player.time -= GameStats.event_type_time[chosen_event_type]
    
def event_chance(road, player):
    happens = random.choices([True, False], weights=GameStats.base_event_probability, k=1)[0]
    if happens:
        trigger_event(road,player)

