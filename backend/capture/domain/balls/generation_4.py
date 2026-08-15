from capture.domain.balls.generation_3 import BaseGenerationThreePlusBallRules
from capture.domain.enums import BallType


class GenerationFourBallRules(BaseGenerationThreePlusBallRules):
    generation = 4
    supported_balls = {
        BallType.POKE_BALL,
        BallType.GREAT_BALL,
        BallType.ULTRA_BALL,
        BallType.MASTER_BALL,
        BallType.FRIEND_BALL,
        BallType.MOON_BALL,
        BallType.FAST_BALL,
        BallType.LOVE_BALL,
        BallType.LEVEL_BALL,
        BallType.LURE_BALL,
        BallType.SPORT_BALL,
        BallType.HEAVY_BALL,
        BallType.PREMIER_BALL,
        BallType.NEST_BALL,
        BallType.REPEAT_BALL,
        BallType.TIMER_BALL,
        BallType.LUXURY_BALL,
        BallType.DIVE_BALL,
        BallType.NET_BALL,
        BallType.DUSK_BALL,
        BallType.HEAL_BALL,
        BallType.QUICK_BALL,
        BallType.CHERISH_BALL,
        BallType.PARK_BALL,
    }
