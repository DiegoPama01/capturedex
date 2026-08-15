from django.test import SimpleTestCase

from capture.domain.calculators.generation_5 import GenerationFiveCalculator
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationFiveCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationFiveCalculator()

    def test_dream_ball_matches_poke_ball_outside_park(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=5,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.SLEEP,
                ball=BallType.DREAM_BALL,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 45)
        self.assertEqual(result.calculation_details["status_multiplier"], 2.5)

    def test_repeat_ball_boosts_previously_caught_species(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=5,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.REPEAT_BALL,
                has_caught_species_before=True,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 157)

    def test_quick_ball_uses_five_times_bonus_on_first_turn(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=5,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.QUICK_BALL,
                turns_elapsed=1,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 225)

    def test_timer_ball_starts_at_one_point_three_multiplier(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=5,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.TIMER_BALL,
                turns_elapsed=1,
            )
        )

        self.assertEqual(result.calculation_details["modified_catch_rate"], 58)

    def test_ultra_ball_is_supported(self) -> None:
        result = self.calculator.calculate(
            CaptureInput(
                generation=5,
                catch_rate=45,
                max_hp=100,
                current_hp=100,
                status=StatusCondition.NONE,
                ball=BallType.ULTRA_BALL,
            )
        )

        self.assertGreater(result.single_throw_probability, 0)
        self.assertEqual(result.calculation_details["shake_checks"], 3)
