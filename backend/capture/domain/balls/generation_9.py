from capture.domain.balls.base import GenerationThreeBallEffect
from capture.domain.balls.context import BallContext
from capture.domain.balls.generation_8 import GenerationEightBallRules
from capture.domain.enums import BallType


class GenerationNineBallRules(GenerationEightBallRules):
    generation = 9

    def resolve(self, context: BallContext) -> GenerationThreeBallEffect:
        if context.ball == BallType.BEAST_BALL:
            multiplier = 5 if context.is_ultra_beast else 0.1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        return super().resolve(context)
