from django.test import SimpleTestCase

from capture.domain.calculators.generation_8 import GenerationEightCalculator
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationEightCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationEightCalculator()

    def test_hisui_ball_is_supported(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=8,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.FEATHER_BALL,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 45)

    def test_legends_origin_ball_is_supported(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=8,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.ORIGIN_BALL,
            )
        )

        self.assertGreater(result.single_throw_probability, 0)
