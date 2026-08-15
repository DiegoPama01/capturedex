from django.test import SimpleTestCase

from capture.domain.calculators.generation_2 import (
    GenerationTwoCalculator,
)
from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput


class GenerationTwoCalculatorTests(SimpleTestCase):
    def setUp(self) -> None:
        self.calculator = GenerationTwoCalculator()

    def test_poke_ball_capture_probability(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.POKE_BALL,
        )

        result = self.calculator.calculate(capture_input)

        # floor(((300 - 200) * 45) / 300) = 15
        # P(captura) = (15 + 1) / 256
        self.assertEqual(
            result.calculation_details["capture_value"],
            15,
        )
        self.assertAlmostEqual(
            result.single_throw_probability,
            16 / 256,
        )

    def test_sleep_adds_ten_to_capture_value(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.SLEEP,
            ball=BallType.POKE_BALL,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["status_bonus"],
            10,
        )
        self.assertEqual(
            result.calculation_details["capture_value"],
            25,
        )

    def test_paralysis_does_not_add_bonus_due_to_glitch(
        self,
    ) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.PARALYSIS,
            ball=BallType.POKE_BALL,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["status_bonus"],
            0,
        )
        self.assertEqual(
            result.calculation_details["capture_value"],
            15,
        )

    def test_great_ball_uses_floored_multiplier(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.GREAT_BALL,
        )

        result = self.calculator.calculate(capture_input)

        # 45 + floor(45 / 2) = 67
        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            67,
        )

    def test_ultra_ball_caps_catch_rate_at_255(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=200,
            max_hp=100,
            current_hp=1,
            status=StatusCondition.SLEEP,
            ball=BallType.ULTRA_BALL,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            255,
        )
        self.assertTrue(result.guaranteed)

    def test_master_ball_is_guaranteed(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=3,
            max_hp=200,
            current_hp=200,
            status=StatusCondition.NONE,
            ball=BallType.MASTER_BALL,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.single_throw_probability,
            1.0,
        )
        self.assertTrue(result.guaranteed)

    def test_friend_ball_matches_poke_ball_rate(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.FRIEND_BALL,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            45,
        )

    def test_moon_ball_quadruples_moon_stone_targets(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.MOON_BALL,
            evolves_with_moon_stone=True,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            180,
        )

    def test_fast_ball_quadruples_fleeing_species(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.FAST_BALL,
            is_fleeing_species=True,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            180,
        )

    def test_love_ball_uses_eight_times_multiplier(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=30,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.LOVE_BALL,
            is_same_species=True,
            is_opposite_gender=True,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            240,
        )

    def test_level_ball_uses_level_comparison(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=30,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.LEVEL_BALL,
            player_pokemon_level=40,
            wild_pokemon_level=10,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            240,
        )

    def test_lure_ball_triples_fishing_encounters(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.LURE_BALL,
            is_fishing_encounter=True,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            135,
        )

    def test_sport_ball_matches_poke_ball_rate(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.SPORT_BALL,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            45,
        )

    def test_heavy_ball_adds_weight_bonus(self) -> None:
        capture_input = CaptureInput(
            generation=2,
            catch_rate=45,
            max_hp=100,
            current_hp=100,
            status=StatusCondition.NONE,
            ball=BallType.HEAVY_BALL,
            wild_pokemon_weight_kg=350,
        )

        result = self.calculator.calculate(capture_input)

        self.assertEqual(
            result.calculation_details["modified_catch_rate"],
            75,
        )
