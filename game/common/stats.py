from game.common.enums import Region, ScannerLevel, TankLevel, TireType


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


    gas_upgrade_cost = {
        TankLevel.level_zero: 0,
        TankLevel.level_one: 300,
        TankLevel.level_two: 900,
        TankLevel.level_three: 2000
    }

    gas_max_level = {
        TankLevel.level_zero: 0,
        TankLevel.level_one: 300,
        TankLevel.level_two: 900,
        TankLevel.level_three: 2000
    }

    tire_traction = {
        TireType.tire_econ: .5,
        TireType.tire_normal: 1,
        TireType.tire_sticky: 1.5
    }

    tire_fuel_efficiancy = {
        TireType.tire_econ: 1.5,
        TireType.tire_normal: 1,
        TireType.tire_sticky: .5
    }

    tire_switch_cost = 300

    game_max_time = 10000

    player_starting_money = 1000

    truck_starting_gas = 1

    truck_starting_max_gas = 1
