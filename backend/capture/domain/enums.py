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

