from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from capture.domain.enums import BallType, StatusCondition
from capture.domain.inputs import CaptureInput
from pokemon.models import PokemonGenerationData

from .serializers import CaptureCalculationInputSerializer

from capture.domain.calculators.factory import (
    get_capture_calculator,
)


class CaptureCalculationView(APIView):
    def post(self, request):
        serializer = CaptureCalculationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        pokemon_data = get_object_or_404(
            PokemonGenerationData.objects.select_related("pokemon"),
            pokemon_id=data["pokemon_id"],
            generation=data["generation"],
            version_group=data["version_group"],
        )
        pokemon_types = set(pokemon_data.pokemon.types)

        capture_input = CaptureInput(
            generation=data["generation"],
            catch_rate=pokemon_data.catch_rate,
            max_hp=data["max_hp"],
            current_hp=data["current_hp"],
            status=StatusCondition(data["status"]),
            ball=BallType(data["ball"]),
            attempts=data["attempts"],
            player_pokemon_level=data.get("player_pokemon_level"),
            wild_pokemon_level=data.get("wild_pokemon_level"),
            wild_pokemon_weight_kg=float(pokemon_data.pokemon.weight_kg),
            wild_pokemon_base_speed=pokemon_data.pokemon.base_speed,
            is_fishing_encounter=data.get("is_fishing_encounter", False),
            is_surfing_encounter=data.get("is_surfing_encounter", False),
            is_underwater_encounter=data.get("is_underwater_encounter", False),
            is_dark_location=data.get("is_dark_location", False),
            has_caught_species_before=data.get("has_caught_species_before", False),
            is_water_type="water" in pokemon_types,
            is_bug_type="bug" in pokemon_types,
            evolves_with_moon_stone=(pokemon_data.pokemon.evolves_with_moon_stone),
            is_fleeing_species=pokemon_data.pokemon.is_fleeing_species,
            is_same_species=data.get("is_same_species", False),
            is_opposite_gender=data.get("is_opposite_gender", False),
            turns_elapsed=data.get("turns_elapsed", 1),
        )

        calculator = get_capture_calculator(data["generation"])
        result = calculator.calculate(capture_input)

        return Response(
            {
                "pokemon": {
                    "id": pokemon_data.pokemon.id,
                    "national_dex_number": (pokemon_data.pokemon.national_dex_number),
                    "name": pokemon_data.pokemon.name,
                    "sprite_url": pokemon_data.sprite_url,
                    "catch_rate": pokemon_data.catch_rate,
                },
                "result": {
                    "single_throw_probability": (result.single_throw_probability),
                    "cumulative_probability": (result.cumulative_probability),
                    "expected_throws": result.expected_throws,
                    "guaranteed": result.guaranteed,
                },
                "calculation_details": result.calculation_details,
            },
            status=status.HTTP_200_OK,
        )
