from capture.domain.balls.base import GenerationThreeBallEffect
from capture.domain.balls.context import BallContext
from capture.domain.balls.generation_6 import GenerationSixBallRules
from capture.domain.enums import BallType


class GenerationEightBallRules(GenerationSixBallRules):
    generation = 8
    supported_balls = GenerationSixBallRules.supported_balls | {
        BallType.BEAST_BALL,
        BallType.FEATHER_BALL,
        BallType.WING_BALL,
        BallType.JET_BALL,
        BallType.HISUI_HEAVY_BALL,
        BallType.LEADEN_BALL,
        BallType.GIGATON_BALL,
        BallType.ORIGIN_BALL,
        BallType.STRANGE_BALL,
    }

    def resolve(self, context: BallContext) -> GenerationThreeBallEffect:
        if context.ball == BallType.BEAST_BALL:
            multiplier = 5 if context.is_ultra_beast else 0.1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball in {
            BallType.FEATHER_BALL,
            BallType.WING_BALL,
            BallType.JET_BALL,
            BallType.HISUI_HEAVY_BALL,
            BallType.LEADEN_BALL,
            BallType.GIGATON_BALL,
            BallType.ORIGIN_BALL,
            BallType.STRANGE_BALL,
        }:
            return self._fixed_multiplier(context.catch_rate, 1)

        return super().resolve(context)
