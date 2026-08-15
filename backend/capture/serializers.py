from rest_framework import serializers
from capture.domain.balls.factory import get_ball_rules
from capture.domain.enums import BallType, StatusCondition
from pokemon.version_groups import (
    DEFAULT_VERSION_GROUP_BY_GENERATION,
    SUPPORTED_VERSION_GROUPS,
)


class CaptureCalculationInputSerializer(serializers.Serializer):
    pokemon_id = serializers.IntegerField(min_value=1)

    generation = serializers.IntegerField(
        min_value=1,
        default=1,
    )

    version_group = serializers.CharField(
        required=False,
    )

    max_hp = serializers.IntegerField(
        min_value=1,
        max_value=999,
    )

    current_hp = serializers.IntegerField(
        min_value=1,
        max_value=999,
    )

    status = serializers.ChoiceField(
        choices=[status.value for status in StatusCondition],
        default=StatusCondition.NONE.value,
    )

    ball = serializers.ChoiceField(
        choices=[ball.value for ball in BallType],
    )

    attempts = serializers.IntegerField(
        min_value=1,
        max_value=1000,
        default=1,
    )

    player_pokemon_level = serializers.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        allow_null=True,
    )

    wild_pokemon_level = serializers.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        allow_null=True,
    )

    is_fishing_encounter = serializers.BooleanField(
        required=False,
        default=False,
    )

    is_surfing_encounter = serializers.BooleanField(
        required=False,
        default=False,
    )

    is_underwater_encounter = serializers.BooleanField(
        required=False,
        default=False,
    )

    is_dark_location = serializers.BooleanField(
        required=False,
        default=False,
    )

    has_caught_species_before = serializers.BooleanField(
        required=False,
        default=False,
    )

    is_same_species = serializers.BooleanField(
        required=False,
        default=False,
    )

    is_opposite_gender = serializers.BooleanField(
        required=False,
        default=False,
    )

    turns_elapsed = serializers.IntegerField(
        min_value=1,
        max_value=100,
        required=False,
        default=1,
    )

    def validate(self, attrs):
        self._validate_hp(attrs)
        self._apply_default_version_group(attrs)
        self._validate_version_group(attrs)
        self._validate_ball(attrs)

        return attrs

    @staticmethod
    def _validate_hp(attrs) -> None:
        if attrs["current_hp"] > attrs["max_hp"]:
            raise serializers.ValidationError(
                {"current_hp": ("Current HP cannot exceed maximum HP.")}
            )

    @staticmethod
    def _apply_default_version_group(attrs) -> None:
        generation = attrs["generation"]

        if (
            "version_group" not in attrs
            and generation in DEFAULT_VERSION_GROUP_BY_GENERATION
        ):
            attrs["version_group"] = DEFAULT_VERSION_GROUP_BY_GENERATION[generation]

    @staticmethod
    def _validate_version_group(attrs) -> None:
        generation = attrs["generation"]
        version_group = attrs["version_group"]

        supported_version_groups = SUPPORTED_VERSION_GROUPS.get(generation)

        if supported_version_groups is None:
            raise serializers.ValidationError(
                {"generation": (f"Generation {generation} is not supported.")}
            )

        if version_group not in supported_version_groups:
            raise serializers.ValidationError(
                {
                    "version_group": (
                        f"Version group '{version_group}' does not "
                        f"belong to Generation {generation}."
                    )
                }
            )

    @staticmethod
    def _validate_ball(attrs) -> None:
        generation = attrs["generation"]
        ball = attrs["ball"]

        supported_balls = get_ball_rules(generation).supported_balls

        if BallType(ball) not in supported_balls:
            raise serializers.ValidationError(
                {
                    "ball": (
                        f"Ball '{ball}' is not supported in Generation {generation}."
                    )
                }
            )
