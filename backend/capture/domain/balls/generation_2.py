from capture.domain.balls.base import (
    BaseBallRules,
    GenerationTwoBallEffect,
)
from capture.domain.balls.context import BallContext
from capture.domain.enums import BallType


class GenerationTwoBallRules(BaseBallRules[GenerationTwoBallEffect]):
    generation = 2
    supported_balls = {
        BallType.POKE_BALL,
        BallType.GREAT_BALL,
        BallType.ULTRA_BALL,
        BallType.MASTER_BALL,
        BallType.FRIEND_BALL,
        BallType.MOON_BALL,
        BallType.FAST_BALL,
        BallType.LOVE_BALL,
        BallType.LEVEL_BALL,
        BallType.LURE_BALL,
        BallType.SPORT_BALL,
        BallType.HEAVY_BALL,
    }

    def resolve(
        self,
        context: BallContext,
    ) -> GenerationTwoBallEffect:
        if context.ball == BallType.MASTER_BALL:
            return GenerationTwoBallEffect(
                modified_catch_rate=255,
                automatic_capture=True,
            )

        if context.ball in {
            BallType.POKE_BALL,
            BallType.FRIEND_BALL,
            BallType.SPORT_BALL,
        }:
            return self._fixed_multiplier(context.catch_rate, 1)

        if context.ball == BallType.GREAT_BALL:
            return GenerationTwoBallEffect(
                modified_catch_rate=min(
                    255,
                    context.catch_rate + context.catch_rate // 2,
                )
            )

        if context.ball == BallType.ULTRA_BALL:
            return self._fixed_multiplier(context.catch_rate, 2)

        if context.ball == BallType.MOON_BALL:
            multiplier = 4 if context.evolves_with_moon_stone else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.FAST_BALL:
            multiplier = 4 if context.is_fleeing_species else 1
            return self._fixed_multiplier(context.catch_rate, multiplier)

        if context.ball == BallType.LOVE_BALL:
            multiplier = 8 if self._love_ball_applies(context) else 1
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
            return GenerationTwoBallEffect(
                modified_catch_rate=self._heavy_ball_catch_rate(context),
            )

        raise ValueError(
            f"Ball {context.ball.value} is not supported in Generation II."
        )

    @staticmethod
    def _fixed_multiplier(
        catch_rate: int,
        multiplier: int,
    ) -> GenerationTwoBallEffect:
        return GenerationTwoBallEffect(
            modified_catch_rate=min(255, catch_rate * multiplier),
        )

    @staticmethod
    def _love_ball_applies(context: BallContext) -> bool:
        return context.is_same_species and context.is_opposite_gender

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
