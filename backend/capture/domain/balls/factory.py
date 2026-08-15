from capture.domain.balls.base import (
    BaseBallRules,
    GenerationOneBallEffect,
    GenerationThreeBallEffect,
    GenerationTwoBallEffect,
)
from capture.domain.balls.generation_1 import GenerationOneBallRules
from capture.domain.balls.generation_2 import GenerationTwoBallRules
from capture.domain.balls.generation_3 import GenerationThreeBallRules
from capture.domain.balls.generation_4 import GenerationFourBallRules
from capture.domain.balls.generation_5 import GenerationFiveBallRules
from capture.domain.balls.generation_6 import GenerationSixBallRules
from capture.domain.balls.generation_7 import GenerationSevenBallRules
from capture.domain.balls.generation_8 import GenerationEightBallRules
from capture.domain.balls.generation_9 import GenerationNineBallRules


_BALL_RULES: dict[
    int,
    type[
        BaseBallRules[
            GenerationOneBallEffect
            | GenerationTwoBallEffect
            | GenerationThreeBallEffect
        ]
    ],
] = {
    1: GenerationOneBallRules,
    2: GenerationTwoBallRules,
    3: GenerationThreeBallRules,
    4: GenerationFourBallRules,
    5: GenerationFiveBallRules,
    6: GenerationSixBallRules,
    7: GenerationSevenBallRules,
    8: GenerationEightBallRules,
    9: GenerationNineBallRules,
}


def get_ball_rules(
    generation: int,
) -> BaseBallRules[
    GenerationOneBallEffect | GenerationTwoBallEffect | GenerationThreeBallEffect
]:
    ball_rules_class = _BALL_RULES.get(generation)

    if ball_rules_class is None:
        raise ValueError(f"Generation {generation} ball rules are not supported.")

    return ball_rules_class()
