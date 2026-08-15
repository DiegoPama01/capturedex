from capture.domain.balls.base import GenerationThreeBallEffect
from capture.domain.balls.context import BallContext
from capture.domain.balls.generation_3 import BaseGenerationThreePlusBallRules
from capture.domain.enums import BallType


class GenerationFiveBallRules(BaseGenerationThreePlusBallRules):
    generation = 5
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
        BallType.DREAM_BALL,
    }

    def resolve(self, context: BallContext) -> GenerationThreeBallEffect:
        if context.ball == BallType.REPEAT_BALL:
            multiplier = 3.5 if context.has_caught_species_before else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.TIMER_BALL:
            multiplier = min(4, 1 + (max(context.turns_elapsed, 1) * 0.3))
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.QUICK_BALL:
            multiplier = 5 if context.turns_elapsed == 1 else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        return super().resolve(context)
