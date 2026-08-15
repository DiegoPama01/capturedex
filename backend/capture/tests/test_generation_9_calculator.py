from django.test import SimpleTestCase

from capture.domain.calculators.generation_9 import GenerationNineCalculator
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationNineCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationNineCalculator()

    def test_beast_ball_is_supported_in_generation_nine(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=9,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.BEAST_BALL,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 4)
