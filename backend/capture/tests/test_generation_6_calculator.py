from django.test import SimpleTestCase

from capture.domain.calculators.generation_6 import GenerationSixCalculator
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationSixCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationSixCalculator()

    def test_sleep_uses_two_point_five_status_multiplier(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=6,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.SLEEP,
                ball=BallType.POKE_BALL,
            )
        )

        self.assertEqual(result.calculation_details["status_multiplier"], 2.5)
        self.assertEqual(result.calculation_details["shake_checks"], 4)

    def test_fast_ball_uses_base_speed_metadata(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=6,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.FAST_BALL,
                wild_pokemon_base_speed=120,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 180)

    def test_lure_ball_uses_five_times_multiplier_when_fishing(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=6,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.LURE_BALL,
                is_fishing_encounter=True,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 225)

    def test_heavy_ball_has_no_special_bonus_in_generation_six(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=6,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.HEAVY_BALL,
                wild_pokemon_weight_kg=400,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 45)
