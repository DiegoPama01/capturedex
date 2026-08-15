from capture.domain.balls.base import GenerationThreeBallEffect
from capture.domain.balls.context import BallContext
from capture.domain.balls.generation_6 import GenerationSixBallRules
from capture.domain.enums import BallType


class GenerationSevenBallRules(GenerationSixBallRules):
    generation = 7
    supported_balls = GenerationSixBallRules.supported_balls | {BallType.BEAST_BALL}

    def resolve(self, context: BallContext) -> GenerationThreeBallEffect:
        if context.ball == BallType.NET_BALL:
            multiplier = 3.5 if context.is_water_type or context.is_bug_type else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.REPEAT_BALL:
            multiplier = 3.5 if context.has_caught_species_before else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.DUSK_BALL:
            multiplier = 3 if context.is_dark_location else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.BEAST_BALL:
            multiplier = 5 if context.is_ultra_beast else 0.1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        return super().resolve(context)
