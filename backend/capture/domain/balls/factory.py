from capture.domain.balls.base import (
    BaseBallRules,
    GenerationOneBallEffect,
    GenerationTwoBallEffect,
)
from capture.domain.balls.generation_1 import GenerationOneBallRules
from capture.domain.balls.generation_2 import GenerationTwoBallRules


_BALL_RULES: dict[
    int,
    type[BaseBallRules[GenerationOneBallEffect | GenerationTwoBallEffect]],
] = {
    1: GenerationOneBallRules,
    2: GenerationTwoBallRules,
}


def get_ball_rules(
    generation: int,
) -> BaseBallRules[GenerationOneBallEffect | GenerationTwoBallEffect]:
    ball_rules_class = _BALL_RULES.get(generation)

    if ball_rules_class is None:
        raise ValueError(f"Generation {generation} ball rules are not supported.")

    return ball_rules_class()
