from rest_framework import serializers

from capture.domain.enums import BallType, StatusCondition


SUPPORTED_VERSION_GROUPS = {
    1: {"red-blue"},
    2: {"gold-silver", "crystal"},
}


class CaptureCalculationInputSerializer(serializers.Serializer):
    pokemon_id = serializers.IntegerField(min_value=1)

    generation = serializers.IntegerField(
        min_value=1,
        default=1,
    )

    version_group = serializers.CharField(
        default="red-blue",
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
        choices=[
            status.value
            for status in StatusCondition
        ],
        default=StatusCondition.NONE.value,
    )

    ball = serializers.ChoiceField(
        choices=[
            ball.value
            for ball in BallType
        ],
    )

    attempts = serializers.IntegerField(
        min_value=1,
        max_value=1000,
        default=1,
    )

    def validate(self, attrs):
        self._validate_hp(attrs)
        self._validate_version_group(attrs)

        return attrs

    @staticmethod
    def _validate_hp(attrs) -> None:
        if attrs["current_hp"] > attrs["max_hp"]:
            raise serializers.ValidationError({
                "current_hp": (
                    "Current HP cannot exceed maximum HP."
                )
            })

    @staticmethod
    def _validate_version_group(attrs) -> None:
        generation = attrs["generation"]
        version_group = attrs["version_group"]

        supported_version_groups = (
            SUPPORTED_VERSION_GROUPS.get(generation)
        )

        if supported_version_groups is None:
            raise serializers.ValidationError({
                "generation": (
                    f"Generation {generation} is not supported."
                )
            })

        if version_group not in supported_version_groups:
            raise serializers.ValidationError({
                "version_group": (
                    f"Version group '{version_group}' does not "
                    f"belong to Generation {generation}."
                )
            })