from rest_framework import serializers

from .models import Pokemon, PokemonGenerationData


class PokemonGenerationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonGenerationData
        fields = (
            "generation",
            "version_group",
            "catch_rate",
            "sprite_url",
        )


class PokemonSerializer(serializers.ModelSerializer):
    generation_data = PokemonGenerationDataSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "national_dex_number",
            "name",
            "slug",
            "generation_data",
        )