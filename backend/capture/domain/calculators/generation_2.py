from typing import cast

from capture.domain.balls.base import GenerationTwoBallEffect
from capture.domain.calculators.base import BaseCaptureCalculator
from capture.domain.balls.context import BallContext
from capture.domain.balls.factory import get_ball_rules
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput
from capture.domain.results import CaptureResult


class GenerationTwoCalculator(BaseCaptureCalculator):
    generation = 2

    _STATUS_BONUSES = {
        StatusCondition.NONE: 0,
        StatusCondition.POISON: 0,
        StatusCondition.BURN: 0,
        StatusCondition.PARALYSIS: 0,
        StatusCondition.SLEEP: 10,
        StatusCondition.FREEZE: 10,
    }

    _SHAKE_THRESHOLDS = (
        (1, 63),
        (2, 75),
        (3, 84),
        (4, 90),
        (5, 95),
        (7, 103),
        (10, 113),
        (15, 126),
        (20, 134),
        (30, 149),
        (40, 160),
        (50, 169),
        (60, 177),
        (80, 191),
        (100, 201),
        (120, 211),
        (140, 220),
        (160, 227),
        (180, 234),
        (200, 240),
        (220, 246),
        (240, 251),
        (254, 253),
        (255, 255),
    )

    def calculate(
        self,
        capture_input: CaptureInput,
    ) -> CaptureResult:
        self._validate_generation(capture_input)

        ball_effect = cast(
            GenerationTwoBallEffect,
            get_ball_rules(self.generation).resolve(
                BallContext(
                    ball=capture_input.ball,
                    catch_rate=capture_input.catch_rate,
                    player_pokemon_level=(capture_input.player_pokemon_level),
                    wild_pokemon_level=capture_input.wild_pokemon_level,
                    wild_pokemon_weight_kg=(capture_input.wild_pokemon_weight_kg),
                    is_fishing_encounter=(capture_input.is_fishing_encounter),
                    evolves_with_moon_stone=(capture_input.evolves_with_moon_stone),
                    is_fleeing_species=capture_input.is_fleeing_species,
                    is_same_species=capture_input.is_same_species,
                    is_opposite_gender=(capture_input.is_opposite_gender),
                )
            ),
        )

        if ball_effect.automatic_capture:
            return self._master_ball_result(capture_input)

        modified_catch_rate = ball_effect.modified_catch_rate

        status_bonus = self._STATUS_BONUSES[capture_input.status]

        capture_value = self._calculate_capture_value(
            max_hp=capture_input.max_hp,
            current_hp=capture_input.current_hp,
            modified_catch_rate=modified_catch_rate,
            status_bonus=status_bonus,
        )

        # El juego genera un entero entre 0 y 255 y captura
        # cuando el resultado es menor o igual que a.
        probability = (capture_value + 1) / 256

        cumulative_probability = 1 - (1 - probability) ** capture_input.attempts

        return CaptureResult(
            single_throw_probability=probability,
            cumulative_probability=cumulative_probability,
            expected_throws=1 / probability,
            guaranteed=capture_value == 255,
            calculation_details={
                "generation": self.generation,
                "ball": capture_input.ball.value,
                "catch_rate": capture_input.catch_rate,
                "modified_catch_rate": modified_catch_rate,
                "status_bonus": status_bonus,
                "capture_value": capture_value,
                "shake_threshold": self._shake_threshold(capture_value),
            },
        )

    def _validate_generation(
        self,
        capture_input: CaptureInput,
    ) -> None:
        if capture_input.generation != self.generation:
            raise ValueError(
                "GenerationTwoCalculator cannot calculate "
                f"Generation {capture_input.generation}."
            )

    @staticmethod
    def _calculate_capture_value(
        *,
        max_hp: int,
        current_hp: int,
        modified_catch_rate: int,
        status_bonus: int,
    ) -> int:
        numerator = (3 * max_hp - 2 * current_hp) * modified_catch_rate
        denominator = 3 * max_hp

        capture_value = (numerator // denominator) + status_bonus

        return max(1, min(255, capture_value))

    @classmethod
    def _shake_threshold(
        cls,
        capture_value: int,
    ) -> int:
        for maximum_capture_value, threshold in cls._SHAKE_THRESHOLDS:
            if capture_value <= maximum_capture_value:
                return threshold

        raise ValueError(f"Invalid capture value: {capture_value}.")

    @staticmethod
    def _master_ball_result(
        capture_input: CaptureInput,
    ) -> CaptureResult:
        return CaptureResult(
            single_throw_probability=1.0,
            cumulative_probability=1.0,
            expected_throws=1.0,
            guaranteed=True,
            calculation_details={
                "generation": 2,
                "ball": BallType.MASTER_BALL.value,
                "capture_value": 255,
                "shake_threshold": 255,
                "automatic_capture": True,
            },
        )
