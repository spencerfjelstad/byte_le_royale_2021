from game.common.enums import *


class GameStats:
    default_road_length = 100

    road_length_maximum_deviation = 20

    region_money_reward_modifier = {
        Region.grass_lands: 1.5,
        Region.nord_dakotia: 1.2,
        Region.mobave_desert: 1,
        Region.mount_vroom: 1,
        Region.lobslantis: .8,
        Region.tropical_cop_land: .5,
    }

    region_renown_reward_modifier = {
        Region.grass_lands: .5,
        Region.nord_dakotia: .8,
        Region.mobave_desert: 1,
        Region.mount_vroom: 1,
        Region.lobslantis: 1.2,
        Region.tropical_cop_land: 1.5,
    }


    # region_difficulty_modifier = {
    #     Region.grass_lands: .5,
    #     Region.nord_dakotia: .6,
    #     Region.mobave_desert: .7,
    #     Region.mount_vroom: .8,
    #     Region.lobslantis: .8,
    #     Region.tropical_cop_land: .9,
    # }

    # objects that can occupy the body slot
    body_objects = [
        ObjectType.tank, #max_gas
        ObjectType.headlights, #animal
        ObjectType.sentryGun #rockslide
    ]

    # objects that can occupy the addon slot
    addonObjects = [
        ObjectType.policeScanner, #police
        ObjectType.rabbitFoot, #all
        ObjectType.GPS #traffic
    ]

    tireObjects = [
        TireType.monster_truck, #bandits
        TireType.tire_econ, #fuel_efficiency
        TireType.tire_normal, #baseline
        TireType.tire_sticky #icy
    ]

    # Tire types are in the enums. Not sure why I did that lol.

    # cost in doollaridoos to upgrade a police scanner
    costs_and_effectiveness = {
        ObjectType.policeScanner: {
            'cost': {
                ScannerLevel.level_zero: 5400,
                ScannerLevel.level_one: 10800,
                ScannerLevel.level_two: 16200,
                ScannerLevel.level_three: 21600
            },

            # error range provided by each scanner
            'effectiveness': {
                ScannerLevel.level_zero: .1,
                ScannerLevel.level_one: .2,
                ScannerLevel.level_two: .35,
                ScannerLevel.level_three: .5
            }
        },

        ObjectType.tank: {
            'cost': {
                TankLevel.level_zero: 5400,
                TankLevel.level_one: 10800,
                TankLevel.level_two: 16200,
                TankLevel.level_three: 21600
            },

            'effectiveness': {
                TankLevel.level_zero: 1,
                TankLevel.level_one: 1.5,
                TankLevel.level_two: 2,
                TankLevel.level_three: 4
            }
        },

        ObjectType.tires: {

            "effectiveness": {
                TireType.tire_econ: 0,
                TireType.tire_normal: 0,
                TireType.tire_sticky: .3,
                TireType.monster_truck: .3
            },

            "fuel_efficiency": {
                TireType.tire_econ: 1.5,
                TireType.tire_normal: 1,
                TireType.tire_sticky: .8,
                TireType.monster_truck: .8
            }
        },


        ObjectType.headlights: {
            "cost": {
                HeadlightLevel.level_zero: 5400,
                HeadlightLevel.level_one: 10800,
                HeadlightLevel.level_two: 16200,
                HeadlightLevel.level_three: 21600
            },

            "effectiveness": {
                HeadlightLevel.level_zero: .1,
                HeadlightLevel.level_one: .2,
                HeadlightLevel.level_two: .35,
                HeadlightLevel.level_three: .5
            }
        },

        ObjectType.sentryGun: {
            "cost": {
                SentryGunLevel.level_zero: 5400,
                SentryGunLevel.level_one: 10800,
                SentryGunLevel.level_two: 16200,
                SentryGunLevel.level_three: 21600
            },
            "effectiveness": {
                SentryGunLevel.level_zero: .1,
                SentryGunLevel.level_one: .2,
                SentryGunLevel.level_two: .35,
                SentryGunLevel.level_three: .5
            }

        },

        ObjectType.rabbitFoot: {
            "cost": {
                RabbitFootLevel.level_zero: 5400,
                RabbitFootLevel.level_one: 10800,
                RabbitFootLevel.level_two: 16200,
                RabbitFootLevel.level_three: 21600
            },

            "effectiveness": {
                RabbitFootLevel.level_zero: .025,
                RabbitFootLevel.level_one: .05,
                RabbitFootLevel.level_two: .1,
                RabbitFootLevel.level_three: .15
            }

        },

        ObjectType.GPS: {
            "cost": {
                GPSLevel.level_zero: 5400,
                GPSLevel.level_one: 10800,
                GPSLevel.level_two: 16200,
                GPSLevel.level_three: 21600
            },

            "effectiveness": {
                GPSLevel.level_zero: .1,
                GPSLevel.level_one: .2,
                GPSLevel.level_two: .35,
                GPSLevel.level_three: .5
            }
        }
    }
    
    possible_event_types = {
        RoadType.mountain_road: {EventType.rock_slide: 40, EventType.animal_in_road: 30, EventType.icy_road: 20, EventType.bounty_hunter: 10, EventType.none: 0},
        RoadType.forest_road: {EventType.animal_in_road: 40, EventType.bounty_hunter: 30, EventType.rock_slide: 20, EventType.icy_road: 10, EventType.none: 0},
        RoadType.tundra_road: {EventType.icy_road: 50, EventType.bounty_hunter: 33, EventType.rock_slide: 17, EventType.none: 0},
        RoadType.city_road: {EventType.bandits: 50, EventType.bounty_hunter: 33, EventType.traffic: 17, EventType.none: 0},
        RoadType.highway: {EventType.bounty_hunter: 67, EventType.traffic: 33, EventType.none: 0},
        RoadType.interstate: {EventType.traffic: 67, EventType.bounty_hunter: 33, EventType.none: 0}
    }

    event_weights = dict()

    for road_type in possible_event_types:
        for event_type in possible_event_types[road_type]:
            if event_type not in event_weights:
                event_weights[event_type] = 0
            event_weights[event_type] += possible_event_types[road_type][event_type]
    animal_chance = event_weights[EventType.animal_in_road]/2400
    bandit_chance = event_weights[EventType.bandits]/2400
    icy_chance = event_weights[EventType.icy_road]/2400
    bounty_hunter_chance = event_weights[EventType.bounty_hunter]/2400
    rockslide_chance = event_weights[EventType.rock_slide]/2400
    traffic_chance = event_weights[EventType.traffic]/2400

    event_type_damage = {
        EventType.animal_in_road: 1/animal_chance,
        EventType.bandits: 1/bandit_chance,
        EventType.icy_road: 1/icy_chance,
        EventType.bounty_hunter: 1/bounty_hunter_chance,
        EventType.rock_slide: 1/rockslide_chance,
        EventType.traffic: 1/traffic_chance,
        EventType.none: 0
    }

    event_type_time = {
        EventType.animal_in_road: event_weights[EventType.animal_in_road] / 20,
        EventType.bandits: event_weights[EventType.bandits] / 20,
        EventType.icy_road: event_weights[EventType.icy_road] / 20,
        EventType.bounty_hunter: event_weights[EventType.bounty_hunter] / 20,
        EventType.rock_slide: event_weights[EventType.rock_slide] / 20,
        EventType.traffic: event_weights[EventType.traffic] / 20,
        EventType.none: 0
    }

    negations = {

        ObjectType.headlights: [EventType.animal_in_road],
        ObjectType.sentryGun: [EventType.rock_slide],
        ObjectType.GPS: [EventType.traffic],
        ObjectType.tank: [],
        ObjectType.policeScanner: [EventType.bounty_hunter],
        TireType.tire_sticky: [EventType.icy_road],
        TireType.tire_normal: [],
        TireType.tire_econ: [],
        TireType.monster_truck: [EventType.bandits],        
        ObjectType.rabbitFoot: [
            EventType.animal_in_road,
            EventType.bandits,
            EventType.icy_road,
            EventType.bounty_hunter,
            EventType.rock_slide,
            EventType.traffic
        ]
    }

    base_event_probability = [25, 75]

    game_max_time = 10000

    player_starting_money = 4000

    truck_starting_gas = 1

    truck_starting_max_gas = 1

    def getMPG(speed):
        return (-0.00249444*(speed**2))+(.2520296*speed)+.22752

    tire_switch_cost = 300

    truck_starting_health = 100

    road_length_variance = .2

    minimum_repair_price = 10

    maximum_repair_price = 30

    minimum_gas_price = 1

    maximum_gas_price = 5

    truck_maximum_speed = 100

    gas_pumping_time_penalty = 5

    repair_pumping_time_penalty = 10

    upgrade_time_penalty = 4

    contract_stats = {
        'node_count': {
            'short': 9,
            'medium': 14,
            'long': 21
        },
        'money_reward': {
            'easy': 3000,
            'medium': 3500,
            'hard': 4200
        },
        'renown_reward': {
            'easy': 20,
            'medium': 30,
            'hard': 39
        },
        'deadline': {
            'short': 3000,
            'medium': 3500,
            'long': 5400
        },
        'difficulty_modifier': {
            ContractDifficulty.easy: 1,
            ContractDifficulty.medium: 1.5,
            ContractDifficulty.hard: 2
        }
    }

    illegal_contract_stats = {
        'risk': {
            ContrabandLevel.level_zero: .10,
            ContrabandLevel.level_one: .20,
            ContrabandLevel.level_two: .30
        },
        'time_penalty': {
            ContrabandLevel.level_zero: 400,
            ContrabandLevel.level_one: 670,
            ContrabandLevel.level_two: 940
        },
        'money_penalty': {
            ContrabandLevel.level_zero: 100,
            ContrabandLevel.level_one: 250,
            ContrabandLevel.level_two: 550
        },
        'reward_modifier': {
            ContrabandLevel.level_zero: 3,
            ContrabandLevel.level_one: 5,
            ContrabandLevel.level_two: 7
        }
    }
