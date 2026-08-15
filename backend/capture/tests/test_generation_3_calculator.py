from django.test import SimpleTestCase

from capture.domain.calculators.generation_3 import GenerationThreeCalculator
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationThreeCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationThreeCalculator()

    def test_net_ball_boosts_water_targets(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=3,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.NET_BALL,
                is_water_type=True,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 135)

    def test_timer_ball_caps_at_four_times_multiplier(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=3,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.TIMER_BALL,
                turns_elapsed=20,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 180)

    def test_master_ball_is_guaranteed(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=3,
                catch_rate=3,
                max_hp=200,
                current_hp=200,
                status=StatusCondition.NONE,
                ball=BallType.MASTER_BALL,
            )
        )

        self.assertEqual(result.single_throw_probability, 1.0)
        self.assertTrue(result.guaranteed)
