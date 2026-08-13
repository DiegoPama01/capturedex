from rest_framework import serializers


SUPPORTED_VERSION_GROUPS = {
    1: {"red-blue"},
    2: {"gold-silver", "crystal"},
}


class PokemonListQuerySerializer(serializers.Serializer):
    generation = serializers.IntegerField(
        min_value=1,
        default=1,
    )
    version_group = serializers.CharField(
        required=False,
    )

    def validate_generation(self, value: int) -> int:
        if value not in SUPPORTED_VERSION_GROUPS:
            raise serializers.ValidationError(f"Generation {value} is not supported.")

        return value

    def validate(self, attrs):
        generation = attrs["generation"]
        version_group = attrs.get("version_group")

        if version_group is None:
            return attrs

        if version_group not in SUPPORTED_VERSION_GROUPS[generation]:
            raise serializers.ValidationError(
                {
                    "version_group": (
                        f"Version group '{version_group}' does not belong "
                        f"to Generation {generation}."
                    )
                }
            )

        return attrs
