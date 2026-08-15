from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from capture.domain.balls.context import BallContext


@dataclass(frozen=True)
class GenerationOneBallEffect:
    random_limit: int
    ball_factor: int
    automatic_capture: bool = False


@dataclass(frozen=True)
class GenerationTwoBallEffect:
    modified_catch_rate: int
    automatic_capture: bool = False


@dataclass(frozen=True)
class GenerationThreeBallEffect:
    modified_catch_rate: int
    automatic_capture: bool = False


BallEffectT = TypeVar("BallEffectT", covariant=True)


class BaseBallRules(ABC, Generic[BallEffectT]):
    generation: int

    @abstractmethod
    def resolve(self, context: BallContext) -> BallEffectT:
        raise NotImplementedError
