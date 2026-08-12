from rest_framework import status
from rest_framework.test import APITestCase

from pokemon.models import Pokemon, PokemonGenerationData


class CaptureCalculationApiTests(APITestCase):
    url = "/api/v1/captures/calculate/"

    def setUp(self) -> None:
        pokemon = Pokemon.objects.create(
            national_dex_number=25,
            name="Pikachu",
            slug="pikachu",
        )

        PokemonGenerationData.objects.create(
            pokemon=pokemon,
            generation=1,
            version_group=(
                PokemonGenerationData.VersionGroup.RED_BLUE
            ),
            catch_rate=190,
            sprite_url="https://example.com/pikachu.png",
        )

        self.valid_payload = {
            "pokemon_id": pokemon.id,
            "generation": 1,
            "max_hp": 100,
            "current_hp": 10,
            "status": "sleep",
            "ball": "ultra_ball",
            "attempts": 5,
        }

    def test_calculates_capture_probability(self) -> None:
        response = self.client.post(
            self.url,
            self.valid_payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["pokemon"]["name"], "Pikachu")
        self.assertEqual(
            response.data["result"]["single_throw_probability"],
            1.0,
        )
        self.assertTrue(response.data["result"]["guaranteed"])

    def test_rejects_current_hp_above_maximum(self) -> None:
        payload = {
            **self.valid_payload,
            "current_hp": 101,
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("current_hp", response.data)

    def test_rejects_invalid_ball(self) -> None:
        payload = {
            **self.valid_payload,
            "ball": "quick_ball",
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("ball", response.data)

    def test_returns_not_found_for_unknown_pokemon(self) -> None:
        payload = {
            **self.valid_payload,
            "pokemon_id": 999999,
        }

        response = self.client.post(
            self.url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )