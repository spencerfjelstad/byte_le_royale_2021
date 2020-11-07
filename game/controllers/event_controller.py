from game.common.stats import GameStats
from game.common.enums import EventType
import random

def trigger_event(road, player):
    # Picks random event type from those possible on given road
    possible_event_type_count = len(GameStats.possible_event_types[road.road_type])
    chosen_event_type = EventType.none
    chosen_event_type = random.choices(GameStats.possible_event_types[road.road_type], weights=GameStats.event_weights[possible_event_type_count], k=1)
    
    # Deal damage based on event
    player.truck.health -= GameStats.event_type_damage[chosen_event_type]
    # Reduce remaining time based on event
    player.time -= GameStats.event_type_time[chosen_event_type]
    


