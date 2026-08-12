from dataclasses import dataclass

from .enums import BallType, StatusCondition


@dataclass(frozen=True)
class CaptureInput:
    generation: int
    catch_rate: int
    max_hp: int
    current_hp: int
    status: StatusCondition
    ball: BallType
    attempts: int = 1

    def __post_init__(self) -> None:
        if self.generation != 1:
            raise ValueError(
                "Only Generation I is currently supported."
            )

        if not 1 <= self.catch_rate <= 255:
            raise ValueError(
                "Catch rate must be between 1 and 255."
            )

        if not 1 <= self.max_hp <= 999:
            raise ValueError(
                "Maximum HP must be between 1 and 999."
            )

        if not 1 <= self.current_hp <= self.max_hp:
            raise ValueError(
                "Current HP must be between 1 and maximum HP."
            )

        if not 1 <= self.attempts <= 1000:
            raise ValueError(
                "Attempts must be between 1 and 1000."
            )