from typing import cast

from capture.domain.balls.base import GenerationOneBallEffect
from capture.domain.calculators.base import BaseCaptureCalculator
from capture.domain.balls.context import BallContext
from capture.domain.balls.factory import get_ball_rules
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput
from capture.domain.results import CaptureResult


class GenerationOneCalculator(BaseCaptureCalculator):
    generation = 1

    _STATUS_BONUSES = {
        StatusCondition.NONE: 0,
        StatusCondition.POISON: 12,
        StatusCondition.BURN: 12,
        StatusCondition.PARALYSIS: 12,
        StatusCondition.SLEEP: 25,
        StatusCondition.FREEZE: 25,
    }

    def calculate(
        self,
        capture_input: CaptureInput,
    ) -> CaptureResult:
        self._validate_generation(capture_input)

        ball_effect = cast(
            GenerationOneBallEffect,
            get_ball_rules(self.generation).resolve(
                BallContext(
                    ball=capture_input.ball,
                    catch_rate=capture_input.catch_rate,
                )
            ),
        )

        if ball_effect.automatic_capture:
            return self._master_ball_result(capture_input)

        random_limit = ball_effect.random_limit
        ball_factor = ball_effect.ball_factor
        status_bonus = self._STATUS_BONUSES[capture_input.status]

        hp_value = self._calculate_hp_value(
            max_hp=capture_input.max_hp,
            current_hp=capture_input.current_hp,
            ball_factor=ball_factor,
        )

        hp_check_probability = 1.0 if hp_value > 255 else (hp_value + 1) / 256

        random_value_count = random_limit + 1

        automatic_success_count = min(
            status_bonus,
            random_value_count,
        )

        first_check_success_count = self._first_check_success_count(
            random_limit=random_limit,
            catch_rate=capture_input.catch_rate,
            status_bonus=status_bonus,
        )

        probability = (
            automatic_success_count / random_value_count
            + first_check_success_count / random_value_count * hp_check_probability
        )

        probability = min(probability, 1.0)

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
                "status_bonus": status_bonus,
                "random_limit": random_limit,
                "ball_factor": ball_factor,
                "hp_value": hp_value,
                "hp_check_probability": hp_check_probability,
            },
        )

    def _validate_generation(
        self,
        capture_input: CaptureInput,
    ) -> None:
        if capture_input.generation != self.generation:
            raise ValueError(
                f"GenerationOneCalculator cannot calculate "
                f"Generation {capture_input.generation}."
            )

    @staticmethod
    def _calculate_hp_value(
        *,
        max_hp: int,
        current_hp: int,
        ball_factor: int,
    ) -> int:
        reduced_current_hp = max(current_hp // 4, 1)

        return ((max_hp * 255) // ball_factor) // reduced_current_hp

    @staticmethod
    def _first_check_success_count(
        *,
        random_limit: int,
        catch_rate: int,
        status_bonus: int,
    ) -> int:
        first_valid_value = status_bonus
        last_valid_value = min(
            random_limit,
            status_bonus + catch_rate,
        )

        if last_valid_value < first_valid_value:
            return 0

        return last_valid_value - first_valid_value + 1

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
                "generation": 1,
                "ball": BallType.MASTER_BALL.value,
                "automatic_capture": True,
            },
        )
