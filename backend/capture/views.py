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
            wild_pokemon_weight_kg=data.get("wild_pokemon_weight_kg"),
            is_fishing_encounter=data.get("is_fishing_encounter", False),
            evolves_with_moon_stone=data.get("evolves_with_moon_stone", False),
            is_fleeing_species=data.get("is_fleeing_species", False),
            is_same_species=data.get("is_same_species", False),
            is_opposite_gender=data.get("is_opposite_gender", False),
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
