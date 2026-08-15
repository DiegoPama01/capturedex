from capture.domain.balls.base import (
    BaseBallRules,
    GenerationOneBallEffect,
)
from capture.domain.balls.context import BallContext
from capture.domain.enums import BallType


class GenerationOneBallRules(BaseBallRules[GenerationOneBallEffect]):
    generation = 1

    _BALL_EFFECTS = {
        BallType.POKE_BALL: GenerationOneBallEffect(
            random_limit=255,
            ball_factor=12,
        ),
        BallType.GREAT_BALL: GenerationOneBallEffect(
            random_limit=200,
            ball_factor=8,
        ),
        BallType.ULTRA_BALL: GenerationOneBallEffect(
            random_limit=150,
            ball_factor=12,
        ),
        BallType.MASTER_BALL: GenerationOneBallEffect(
            random_limit=0,
            ball_factor=0,
            automatic_capture=True,
        ),
    }

    def resolve(
        self,
        context: BallContext,
    ) -> GenerationOneBallEffect:
        effect = self._BALL_EFFECTS.get(context.ball)

        if effect is None:
            raise ValueError(
                f"Ball {context.ball.value} is not supported in Generation I."
            )

        return effect
