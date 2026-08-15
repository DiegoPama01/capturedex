from capture.domain.balls.base import BaseBallRules, GenerationThreeBallEffect
from capture.domain.balls.context import BallContext
from capture.domain.enums import BallType


class BaseGenerationThreePlusBallRules(BaseBallRules[GenerationThreeBallEffect]):
    generation: int
    supported_balls: set[BallType]

    _POKE_BALLS = {
        BallType.POKE_BALL,
        BallType.FRIEND_BALL,
        BallType.LUXURY_BALL,
        BallType.PREMIER_BALL,
        BallType.HEAL_BALL,
        BallType.CHERISH_BALL,
        BallType.PARK_BALL,
        BallType.SPORT_BALL,
    }

    def resolve(self, context: BallContext) -> GenerationThreeBallEffect:
        if context.ball not in self.supported_balls:
            raise ValueError(
                f"Ball {context.ball.value} is not supported in Generation {self.generation}."
            )

        if context.ball == BallType.MASTER_BALL:
            return GenerationThreeBallEffect(
                modified_catch_rate=255,
                automatic_capture=True,
            )

        if context.ball in self._POKE_BALLS:
            return self._fixed_multiplier(context.catch_rate, 1)

        if context.ball == BallType.GREAT_BALL:
            return self._fixed_multiplier(context.catch_rate, 1.5)

        if context.ball == BallType.ULTRA_BALL:
            return self._fixed_multiplier(context.catch_rate, 2)

        if context.ball == BallType.NET_BALL:
            multiplier = 3 if context.is_water_type or context.is_bug_type else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.DIVE_BALL:
            applies = (
                context.is_fishing_encounter
                or context.is_surfing_encounter
                or context.is_underwater_encounter
            )
            return self._fixed_multiplier(context.catch_rate, 3.5 if applies else 1)

        if context.ball == BallType.NEST_BALL:
            return self._fixed_multiplier(
                context.catch_rate,
                self._nest_ball_multiplier(context),
            )

        if context.ball == BallType.REPEAT_BALL:
            multiplier = 3 if context.has_caught_species_before else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.TIMER_BALL:
            return self._fixed_multiplier(
                context.catch_rate,
                self._timer_ball_multiplier(context.turns_elapsed),
            )

        if context.ball == BallType.MOON_BALL:
            multiplier = 4 if context.evolves_with_moon_stone else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.FAST_BALL:
            multiplier = 4 if context.is_fleeing_species else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.LOVE_BALL:
            multiplier = (
                8 if context.is_same_species and context.is_opposite_gender else 1
            )
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.LEVEL_BALL:
            return self._fixed_multiplier(
                context.catch_rate,
                self._level_ball_multiplier(context),
            )

        if context.ball == BallType.LURE_BALL:
            multiplier = 3 if context.is_fishing_encounter else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.HEAVY_BALL:
            return GenerationThreeBallEffect(
                modified_catch_rate=self._heavy_ball_catch_rate(context),
            )

        if context.ball == BallType.DUSK_BALL:
            multiplier = 3.5 if context.is_dark_location else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.QUICK_BALL:
            multiplier = 4 if context.turns_elapsed == 1 else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.DREAM_BALL:
            return self._fixed_multiplier(context.catch_rate, 1)

        raise ValueError(f"Ball {context.ball.value} has no configured effect.")

    @staticmethod
    def _fixed_multiplier(
        catch_rate: int, multiplier: float
    ) -> GenerationThreeBallEffect:
        return GenerationThreeBallEffect(
            modified_catch_rate=max(1, min(255, int(catch_rate * multiplier))),
        )

    @staticmethod
    def _nest_ball_multiplier(context: BallContext) -> float:
        if context.wild_pokemon_level is None:
            return 1

        return max(1, (41 - context.wild_pokemon_level) / 10)

    @staticmethod
    def _timer_ball_multiplier(turns_elapsed: int) -> float:
        return min(4, 1 + (max(turns_elapsed, 1) - 1) * 0.3)

    @staticmethod
    def _level_ball_multiplier(context: BallContext) -> int:
        if context.player_pokemon_level is None or context.wild_pokemon_level is None:
            return 1

        if context.player_pokemon_level >= context.wild_pokemon_level * 4:
            return 8

        if context.player_pokemon_level >= context.wild_pokemon_level * 2:
            return 4

        if context.player_pokemon_level > context.wild_pokemon_level:
            return 2

        return 1

    @staticmethod
    def _heavy_ball_catch_rate(context: BallContext) -> int:
        if context.wild_pokemon_weight_kg is None:
            return context.catch_rate

        if context.wild_pokemon_weight_kg < 102.4:
            catch_rate = context.catch_rate - 20
        elif context.wild_pokemon_weight_kg < 204.8:
            catch_rate = context.catch_rate
        elif context.wild_pokemon_weight_kg < 307.2:
            catch_rate = context.catch_rate + 20
        elif context.wild_pokemon_weight_kg < 409.6:
            catch_rate = context.catch_rate + 30
        else:
            catch_rate = context.catch_rate + 40

        return max(1, min(255, catch_rate))


class GenerationThreeBallRules(BaseGenerationThreePlusBallRules):
    generation = 3
    supported_balls = {
        BallType.POKE_BALL,
        BallType.GREAT_BALL,
        BallType.ULTRA_BALL,
        BallType.MASTER_BALL,
        BallType.PREMIER_BALL,
        BallType.NEST_BALL,
        BallType.REPEAT_BALL,
        BallType.TIMER_BALL,
        BallType.LUXURY_BALL,
        BallType.DIVE_BALL,
        BallType.NET_BALL,
    }
