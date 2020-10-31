from game.common.stats import GameStats
from game.common.enums import EventType
import random

def trigger_event(road, player):
    # Picks random event type from those possible on given road
    possible_event_type_count = len(GameStats.possible_event_types[road.road_type])
    chosen_event_type = EventType.none
    if possible_event_type_count == 4:
        chosen_event_type = random.choices(GameStats.possible_event_types[road.road_type], weights=[4,3,2,1], k=1)
    if possible_event_type_count == 3:
        chosen_event_type = random.choices(GameStats.possible_event_types[road.road_type], weights=[3,2,1], k=1)
    if possible_event_type_count == 2:
        chosen_event_type = random.choices(GameStats.possible_event_types[road.road_type], weights=[2,1], k=1)
    # Deal damage based on event
    player.truck.health -= GameStats.event_type_damage[chosen_event_type]
    # Reduce remaining time based on event
    player.time -= GameStats.event_type_time[chosen_event_type]
    


