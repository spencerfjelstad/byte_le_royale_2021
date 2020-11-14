from game.common.enums import *
from game.common.truck import Truck

class GameStats:
    default_road_length = 100

    region_reward_modifier = {
        Region.grass_lands: .5,
        Region.nord_dakotia: .6,
        Region.mobave_desert: .7,
        Region.mount_vroom: .8,
        Region.lobslantis: .8,
        Region.tropical_cop_land: .9,
    }

    region_difficulty_modifier = {
        Region.grass_lands: .5,
        Region.nord_dakotia: .6,
        Region.mobave_desert: .7,
        Region.mount_vroom: .8,
        Region.lobslantis: .8,
        Region.tropical_cop_land: .9,
    }

    road_type_length_modifier = {
        RoadType.mountain_road: 1,
        RoadType.forest_road: 1,
        RoadType.tundra_road: 1.5,
        RoadType.city_road: 1.5,
        RoadType.highway: 2,
        RoadType.interstate: 2
    }

    possible_event_types = {
        RoadType.mountain_road: [EventType.rock_slide, EventType.animal_in_road, EventType.icy_road, EventType.police, EventType.none],
        RoadType.forest_road: [EventType.animal_in_road, EventType.police, EventType.rock_slide, EventType.icy_road, EventType.none],
        RoadType.tundra_road: [EventType.icy_road, EventType.police, EventType.rock_slide, EventType.none],
        RoadType.city_road: [EventType.bandits, EventType.police, EventType.traffic, EventType.none],
        RoadType.highway: [EventType.police, EventType.traffic, EventType.none],
        RoadType.interstate: [EventType.traffic, EventType.police, EventType.none]
    }

    event_weights = {
        RoadType.mountain_road:[40 - Truck.event_type_bonus[EventType.rock_slide], 30 - Truck.event_type_bonus[EventType.animal_in_road],\
            20 - Truck.event_type_bonus[EventType.icy_road], 10 - Truck.event_type_bonus[EventType.police], 0 + Truck.total_mountain_bonuses],
        RoadType.forest_road:[40 - Truck.event_type_bonus[EventType.animal_in_road], 30 - Truck.event_type_bonus[EventType.police],\
            20 - Truck.event_type_bonus[EventType.rock_slide], 10 - Truck.event_type_bonus[EventType.icy_road], 0 + Truck.total_forest_bonuses],
        RoadType.tundra_road:[50 - Truck.event_type_bonus[EventType.icy_road], 33 - Truck.event_type_bonus[EventType.police],\
            17 - Truck.event_type_bonus[EventType.rock_slide], 0 + Truck.total_tundra_bonuses],
        RoadType.city_road:[50 - Truck.event_type_bonus[EventType.bandits], 33 - Truck.event_type_bonus[EventType.police],\
            17 - Truck.event_type_bonus[EventType.traffic], 0 + Truck.total_city_bonuses],
        RoadType.highway:[67 - Truck.event_type_bonus[EventType.police], 33 - Truck.event_type_bonus[EventType.traffic],\
            0 + Truck.total_highway_bonuses],
        RoadType.interstate:[67 - Truck.event_type_bonus[EventType.traffic], 33 - Truck.event_type_bonus[EventType.police],\
            0 + Truck.total_interstate_bonuses]
    }

    event_type_damage = {
        EventType.animal_in_road: 10,
        EventType.bandits: 20,
        EventType.icy_road: 5,
        EventType.police: 5,
        EventType.rock_slide: 5,
        EventType.traffic: 5,
        EventType.none: 0 
    }

    event_type_time = {
        EventType.animal_in_road: 5,
        EventType.bandits: 5,
        EventType.icy_road: 10,
        EventType.police: 20,
        EventType.rock_slide: 10,
        EventType.traffic: 20,
        EventType.none: 0
    }

    base_event_probability = [25, 75]

    game_max_time = 10000

    player_starting_money = 1000

    truck_starting_gas = 1

    truck_starting_max_gas = 1

    truck_starting_health = 50
