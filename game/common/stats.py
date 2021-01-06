from game.common.enums import *


class GameStats:
    default_road_length = 100

    road_length_maximum_deviation = 20

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

    # objects that can occupy the body slot
    body_objects = [
        ObjectType.tank,
        ObjectType.headlights,
        ObjectType.sentryGun
    ]

    # objects that can occupy the addon slot
    addonObjects = [
        ObjectType.policeScanner,
        ObjectType.rabbitFoot,
        ObjectType.GPS
    ]

    # Tire types are in the enums. Not sure why I did that lol.

    # cost in doollaridoos to upgrade a police scanner
    scanner_upgrade_cost = {
        ScannerLevel.level_zero: 0,
        ScannerLevel.level_one: 300,
        ScannerLevel.level_two: 900,
        ScannerLevel.level_three: 2000
    }

    # error range provided by each scanner
    scanner_ranges = {
        ScannerLevel.level_zero: 100,
        ScannerLevel.level_one: 50,
        ScannerLevel.level_two: 20,
        ScannerLevel.level_three: 1
    }

    tank_upgrade_cost = {
        TankLevel.level_zero: 10,
        TankLevel.level_one: 300,
        TankLevel.level_two: 900,
        TankLevel.level_three: 2000
    }

    gas_max_level = {
        TankLevel.level_zero: 10,
        TankLevel.level_one: 300,
        TankLevel.level_two: 900,
        TankLevel.level_three: 2000
    }

    tire_traction = {
        TireType.tire_econ: .5,
        TireType.tire_normal: 1,
        TireType.tire_sticky: 1.5
    }

    tire_fuel_efficiency = {
        TireType.tire_econ: 1.5,
        TireType.tire_normal: 1,
        TireType.tire_sticky: .5
    }

    headlight_upgrade_cost = {
        HeadlightLevel.level_zero: 10,
        HeadlightLevel.level_one: 50,
        HeadlightLevel.level_two: 100,
        HeadlightLevel.level_three: 300
    }

    headlight_effectiveness = {
        HeadlightLevel.level_zero: .1,
        HeadlightLevel.level_one: .3,
        HeadlightLevel.level_two: .7,
        HeadlightLevel.level_three: .9
    }

    sentry_upgrade_cost = {
        SentryGunLevel.level_zero: 10,
        SentryGunLevel.level_one: 50,
        SentryGunLevel.level_two: 100,
        SentryGunLevel.level_three: 300
    }

    sentry_DPM = {
        SentryGunLevel.level_zero: 100,
        SentryGunLevel.level_one: 1000,
        SentryGunLevel.level_two: 10000,
        SentryGunLevel.level_three: 300000
    }

    rabbit_foot_upgrade_cost = {
        RabbitFootLevel.level_zero: 10,
        RabbitFootLevel.level_one: 20,
        RabbitFootLevel.level_two: 40,
        RabbitFootLevel.level_three: 80
    }

    rabbit_foot_luck_level = {
        RabbitFootLevel.level_zero: .1,
        RabbitFootLevel.level_one: .2,
        RabbitFootLevel.level_two: .25,
        RabbitFootLevel.level_three: .27
    }

    GPS_upgrade_cost = {
        GPSLevel.level_zero: 100,
        GPSLevel.level_one: 200,
        GPSLevel.level_two: 700,
        GPSLevel.level_three: 1400
    }

    GPS_accuracy = {
        GPSLevel.level_zero: .33,
        GPSLevel.level_one: .5,
        GPSLevel.level_two: .58,
        GPSLevel.level_three: .65
    }

    tire_switch_cost = 300
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
        #Order for corresponding event type listed above list
        #Mountain order: rock slide, animal in road, icy road, police, none
        RoadType.mountain_road:[40, 30, 20, 10, 0],
        #Forest order: animal in road, police, rock slide, icy road, none
        RoadType.forest_road:[40, 30, 20, 10, 0],
        #Tundra order: icy road, police, rock slide, none
        RoadType.tundra_road:[50, 33, 17, 0],
        #City order: bandits, police, traffic, none
        RoadType.city_road:[50, 33, 17, 0],
        #Highway order: police, traffic, none
        RoadType.highway:[67, 33, 0],
        #Interstate order: traffic, police, none
        RoadType.interstate:[67, 33, 0]
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

    headlights_negates = {
        EventType.animal_in_road: (0, 1),
        EventType.traffic: (0, 20),
        EventType.police: (1, 20)
        EventType.rock_slide: (2, 9)
    }

    sentry_gun_negates = {
        EventType.bandits: (0, 2),
        EventType.police: (0, 2),
        EventType.animal_in_road: (0, 2)
    }

    gps_negates = {
        EventType.bandits: (0,0),
        EventType.traffic: (0, 10),
        EventType.rock_slide: (0, 5),
        EventType.police: (0,0)
    }

    police_scanner_negates = {
        EventType.police: (0,0),
        EventType.bandits: (0,0),
        EventType.rock_slide: (2, 6)
    }

    rabbit_foot_negates = {
        
    }

    base_event_probability = [25, 75]

    game_max_time = 10000

    player_starting_money = 1000

    truck_starting_gas = 1

    truck_starting_max_gas = 1

    truck_starting_health = 50
