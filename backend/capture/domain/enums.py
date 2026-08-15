from enum import StrEnum


class StatusCondition(StrEnum):
    NONE = "none"
    POISON = "poison"
    BURN = "burn"
    PARALYSIS = "paralysis"
    SLEEP = "sleep"
    FREEZE = "freeze"


class BallType(StrEnum):
    POKE_BALL = "poke_ball"
    GREAT_BALL = "great_ball"
    ULTRA_BALL = "ultra_ball"
    MASTER_BALL = "master_ball"
    FRIEND_BALL = "friend_ball"
    MOON_BALL = "moon_ball"
    FAST_BALL = "fast_ball"
    LOVE_BALL = "love_ball"
    LEVEL_BALL = "level_ball"
    LURE_BALL = "lure_ball"
    SPORT_BALL = "sport_ball"
    HEAVY_BALL = "heavy_ball"
    PREMIER_BALL = "premier_ball"
    NEST_BALL = "nest_ball"
    REPEAT_BALL = "repeat_ball"
    TIMER_BALL = "timer_ball"
    LUXURY_BALL = "luxury_ball"
    DIVE_BALL = "dive_ball"
    NET_BALL = "net_ball"
    DUSK_BALL = "dusk_ball"
    HEAL_BALL = "heal_ball"
    QUICK_BALL = "quick_ball"
    CHERISH_BALL = "cherish_ball"
    PARK_BALL = "park_ball"
    DREAM_BALL = "dream_ball"
