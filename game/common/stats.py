from game.common.enums import LocationType


class GameStats:
    location_reward_modifier = {
        LocationType.grass_lands: .5,
        LocationType.nord_dakotia: .6,
        LocationType.mobave_desert: .7,
        LocationType.mount_vroom: .8,
        LocationType.loblantis: .8,
        LocationType.tropical_cop_land: .9,
    }

    location_difficulty_modifier = {
        LocationType.grass_lands: .5,
        LocationType.nord_dakotia: .6,
        LocationType.mobave_desert: .7,
        LocationType.mount_vroom: .8,
        LocationType.loblantis: .8,
        LocationType.tropical_cop_land: .9,
    }
