from game.common.enums import NodeType


class GameStats:
    node_reward_modifier = {
        NodeType.grass_lands: .5,
        NodeType.nord_dakotia: .6,
        NodeType.mobave_desert: .7,
        NodeType.mount_vroom: .8,
        NodeType.loblantis: .8,
        NodeType.tropical_cop_land: .9,
    }

    node_difficulty_modifier = {
        NodeType.grass_lands: .5,
        NodeType.nord_dakotia: .6,
        NodeType.mobave_desert: .7,
        NodeType.mount_vroom: .8,
        NodeType.loblantis: .8,
        NodeType.tropical_cop_land: .9,
    }
