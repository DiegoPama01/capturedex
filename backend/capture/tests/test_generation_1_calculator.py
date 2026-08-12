# capture/tests/test_generation_1_calculator.py

from django.test import SimpleTestCase

from capture.domain.calculators.generation_1 import (
    GenerationOneCalculator,
)
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationOneCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationOneCalculator()

    def test_sleeping_pokemon_with_ultra_ball(self) -> None:
        capture_input = CaptureInput(
            generation=1,
            catch_rate=45,
            max_hp=100,
            current_hp=10,
            status=StatusCondition.SLEEP,
            ball=BallType.ULTRA_BALL,
            attempts=5,
        )

        result = self.calculator.calculate(capture_input)

        self.assertAlmostEqual(
            result.single_throw_probability,
            71 / 151,
        )
        self.assertAlmostEqual(
            result.cumulative_probability,
            1 - (1 - 71 / 151) ** 5,
        )
        self.assertFalse(result.guaranteed)

    def test_master_ball_is_guaranteed(self) -> None:
        capture_input = CaptureInput(
            generation=1,
            catch_rate=3,
            max_hp=200,
            current_hp=200,
            status=StatusCondition.NONE,
            ball=BallType.MASTER_BALL,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(result.single_throw_probability, 1.0)
        self.assertEqual(result.cumulative_probability, 1.0)
        self.assertEqual(result.expected_throws, 1.0)
        self.assertTrue(result.guaranteed)
        
    def test_great_ball_can_outperform_ultra_ball(self) -> None:
        common_data = {
            "generation": 1,
            "catch_rate": 45,
            "max_hp": 100,
            "current_hp": 100,
            "status": StatusCondition.NONE,
        }

        great_ball_result = self.calculator.calculate(
            CaptureInput(
                **common_data,
                ball=BallType.GREAT_BALL,
            )
        )

        ultra_ball_result = self.calculator.calculate(
            CaptureInput(
                **common_data,
                ball=BallType.ULTRA_BALL,
            )
        )

        self.assertGreater(
            great_ball_result.single_throw_probability,
            ultra_ball_result.single_throw_probability,
    )