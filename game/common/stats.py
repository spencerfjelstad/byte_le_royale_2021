from game.common.enums import *

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
        RoadType.mountain_road: [EventType.rock_slide, EventType.animal_in_road, EventType.icy_road, EventType.police],
        RoadType.forest_road: [EventType.animal_in_road, EventType.police, EventType.rock_slide, EventType.icy_road],
        RoadType.tundra_road: [EventType.icy_road, EventType.police, EventType.rock_slide],
        RoadType.city_road: [EventType.bandits, EventType.police, EventType.traffic],
        RoadType.highway: [EventType.police, EventType.traffic],
        RoadType.interstate: [EventType.traffic, EventType.police]
    }

    event_weights = {
        4:[4,3,2,1],
        3:[3,2,1],
        2:[2,1]
    }

    event_type_damage = {
        EventType.animal_in_road: 10,
        EventType.bandits: 20,
        EventType.icy_road: 5,
        EventType.police: 5,
        EventType.rock_slide: 5,
        EventType.traffic: 5  
    }

    event_type_time = {
        EventType.animal_in_road: 5,
        EventType.bandits: 5,
        EventType.icy_road: 10,
        EventType.police: 20,
        EventType.rock_slide: 10,
        EventType.traffic: 20
    }

    game_max_time = 10000

    player_starting_money = 1000

    truck_starting_gas = 1

    truck_starting_max_gas = 1

    truck_starting_health = 50
