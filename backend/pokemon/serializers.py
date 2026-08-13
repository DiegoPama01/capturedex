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
    generation_data = serializers.SerializerMethodField()

    def get_generation_data(self, obj):
        generation_data = getattr(
            obj,
            "filtered_generation_data",
            obj.generation_data.all(),
        )
        return PokemonGenerationDataSerializer(generation_data, many=True).data

    class Meta:
        model = Pokemon
        fields = (
            "id",
            "national_dex_number",
            "name",
            "slug",
            "generation_data",
        )
