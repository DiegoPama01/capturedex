from capture.domain.balls.base import GenerationThreeBallEffect
from capture.domain.balls.context import BallContext
from capture.domain.balls.generation_3 import BaseGenerationThreePlusBallRules
from capture.domain.enums import BallType


class GenerationSixBallRules(BaseGenerationThreePlusBallRules):
    generation = 6
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
        if context.ball == BallType.NET_BALL:
            multiplier = 3 if context.is_water_type or context.is_bug_type else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.NEST_BALL:
            multiplier = self._nest_ball_multiplier_generation_six(context)
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.REPEAT_BALL:
            multiplier = 3 if context.has_caught_species_before else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.FAST_BALL:
            multiplier = 4 if (context.wild_pokemon_base_speed or 0) >= 100 else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.LURE_BALL:
            multiplier = 5 if context.is_fishing_encounter else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.HEAVY_BALL:
            return self._fixed_multiplier(context.catch_rate, 1)

        if context.ball == BallType.QUICK_BALL:
            multiplier = 5 if context.turns_elapsed == 1 else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        return super().resolve(context)

    @staticmethod
    def _nest_ball_multiplier_generation_six(context: BallContext) -> float:
        if context.wild_pokemon_level is None or context.wild_pokemon_level >= 30:
            return 1

        return max(1, (41 - context.wild_pokemon_level) / 10)
