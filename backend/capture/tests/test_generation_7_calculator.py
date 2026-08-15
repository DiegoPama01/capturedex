from django.test import SimpleTestCase

from capture.domain.calculators.generation_7 import GenerationSevenCalculator
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationSevenCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationSevenCalculator()

    def test_repeat_ball_uses_three_point_five_multiplier(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=7,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.REPEAT_BALL,
                has_caught_species_before=True,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 157)

    def test_beast_ball_defaults_to_point_one_multiplier(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=7,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.BEAST_BALL,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 4)

    def test_beast_ball_boosts_ultra_beasts(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=7,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.BEAST_BALL,
                is_ultra_beast=True,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 225)
