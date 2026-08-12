from rest_framework import serializers

from capture.domain.enums import BallType, StatusCondition


class CaptureCalculationInputSerializer(serializers.Serializer):
    pokemon_id = serializers.IntegerField(min_value=1)
    generation = serializers.IntegerField(
        min_value=1,
        max_value=1,
        default=1,
    )
    max_hp = serializers.IntegerField(min_value=1, max_value=999)
    current_hp = serializers.IntegerField(min_value=1, max_value=999)
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

    def validate(self, attrs):
        if attrs["current_hp"] > attrs["max_hp"]:
            raise serializers.ValidationError({
                "current_hp": (
                    "Current HP cannot exceed maximum HP."
                )
            })

        return attrs