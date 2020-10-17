from game.common.enums import Region
from game.common.enums import RoadType
from game.common.enums import DisasterType

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

    road_length_modifier = {
        RoadType.mountain_road: 1,
        RoadType.forest_road: 1,
        RoadType.tundra_road: 1.5,
        RoadType.city_road: 1.5,
        RoadType.highway: 2,
        RoadType.interstate: 2
    }


