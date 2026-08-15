import math
from typing import cast

from capture.domain.balls.base import GenerationThreeBallEffect
from capture.domain.balls.context import BallContext
from capture.domain.balls.factory import get_ball_rules
from capture.domain.calculators.base import BaseCaptureCalculator
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput
from capture.domain.results import CaptureResult


class BaseGenerationThreePlusCalculator(BaseCaptureCalculator):
    generation: int

    _STATUS_MULTIPLIERS = {
        StatusCondition.NONE: 1.0,
        StatusCondition.POISON: 1.5,
        StatusCondition.BURN: 1.5,
        StatusCondition.PARALYSIS: 1.5,
        StatusCondition.SLEEP: 2.0,
        StatusCondition.FREEZE: 2.0,
    }

    def calculate(self, capture_input: CaptureInput) -> CaptureResult:
        self._validate_generation(capture_input)

        ball_effect = cast(
            GenerationThreeBallEffect,
            get_ball_rules(self.generation).resolve(
                BallContext(
                    ball=capture_input.ball,
                    catch_rate=capture_input.catch_rate,
                    status=capture_input.status.value,
                    player_pokemon_level=capture_input.player_pokemon_level,
                    wild_pokemon_level=capture_input.wild_pokemon_level,
                    wild_pokemon_weight_kg=capture_input.wild_pokemon_weight_kg,
                    is_fishing_encounter=capture_input.is_fishing_encounter,
                    is_surfing_encounter=capture_input.is_surfing_encounter,
                    is_underwater_encounter=capture_input.is_underwater_encounter,
                    is_dark_location=capture_input.is_dark_location,
                    has_caught_species_before=capture_input.has_caught_species_before,
                    is_water_type=capture_input.is_water_type,
                    is_bug_type=capture_input.is_bug_type,
                    evolves_with_moon_stone=capture_input.evolves_with_moon_stone,
                    is_fleeing_species=capture_input.is_fleeing_species,
                    is_same_species=capture_input.is_same_species,
                    is_opposite_gender=capture_input.is_opposite_gender,
                    turns_elapsed=capture_input.turns_elapsed,
                )
            ),
        )

        if ball_effect.automatic_capture:
            return self._master_ball_result()

        status_multiplier = self._STATUS_MULTIPLIERS[capture_input.status]
        capture_value = self._calculate_capture_value(
            max_hp=capture_input.max_hp,
            current_hp=capture_input.current_hp,
            modified_catch_rate=ball_effect.modified_catch_rate,
            status_multiplier=status_multiplier,
        )

        if capture_value >= 255:
            probability = 1.0
            shake_check_value = 65535
        else:
            shake_check_value = self._calculate_shake_check_value(capture_value)
            probability = ((shake_check_value + 1) / 65536) ** 4

        cumulative_probability = 1 - (1 - probability) ** capture_input.attempts

        return CaptureResult(
            single_throw_probability=probability,
            cumulative_probability=cumulative_probability,
            expected_throws=1 / probability,
            guaranteed=probability == 1.0,
            calculation_details={
                "generation": self.generation,
                "ball": capture_input.ball.value,
                "catch_rate": capture_input.catch_rate,
                "modified_catch_rate": ball_effect.modified_catch_rate,
                "status_multiplier": status_multiplier,
                "capture_value": capture_value,
                "shake_check_value": shake_check_value,
            },
        )

    def _validate_generation(self, capture_input: CaptureInput) -> None:
        if capture_input.generation != self.generation:
            raise ValueError(
                f"{self.__class__.__name__} cannot calculate "
                f"Generation {capture_input.generation}."
            )

    @staticmethod
    def _calculate_capture_value(
        *,
        max_hp: int,
        current_hp: int,
        modified_catch_rate: int,
        status_multiplier: float,
    ) -> int:
        numerator = (3 * max_hp - 2 * current_hp) * modified_catch_rate
        denominator = 3 * max_hp
        base_value = numerator // denominator

        return max(1, min(255, int(base_value * status_multiplier)))

    @staticmethod
    def _calculate_shake_check_value(capture_value: int) -> int:
        interim_value = 16711680 / capture_value
        return int(1048560 / math.sqrt(math.sqrt(interim_value)))

    def _master_ball_result(self) -> CaptureResult:
        return CaptureResult(
            single_throw_probability=1.0,
            cumulative_probability=1.0,
            expected_throws=1.0,
            guaranteed=True,
            calculation_details={
                "generation": self.generation,
                "ball": BallType.MASTER_BALL.value,
                "capture_value": 255,
                "shake_check_value": 65535,
                "automatic_capture": True,
            },
        )


class GenerationThreeCalculator(BaseGenerationThreePlusCalculator):
    generation = 3
