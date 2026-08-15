from django.test import SimpleTestCase

from capture.domain.calculators.generation_4 import GenerationFourCalculator
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationFourCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationFourCalculator()

    def test_dusk_ball_boosts_dark_locations(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=4,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.DUSK_BALL,
                is_dark_location=True,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 157)

    def test_quick_ball_only_boosts_first_turn(self) -> None:
        boosted_result = self.calculator.calculate(
            CaptureInput(
                generation=4,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.QUICK_BALL,
                turns_elapsed=1,
            )
        )
        neutral_result = self.calculator.calculate(
            CaptureInput(
                generation=4,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.QUICK_BALL,
                turns_elapsed=2,
            )
        )

        self.assertEqual(boosted_result.calculation_details["modified_catch_rate"], 180)
        self.assertEqual(neutral_result.calculation_details["modified_catch_rate"], 45)

    def test_heavy_ball_uses_weight_bonus(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=4,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.HEAVY_BALL,
                wild_pokemon_weight_kg=350,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 75)
