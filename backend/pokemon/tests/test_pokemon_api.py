from rest_framework import status
from rest_framework.test import APITestCase

from pokemon.models import Pokemon, PokemonGenerationData


class PokemonListApiTests(APITestCase):
    url = "/api/v1/pokemon/"

    def setUp(self) -> None:
        bulbasaur = Pokemon.objects.create(
            national_dex_number=1,
            name="Bulbasaur",
            slug="bulbasaur",
        )
        chikorita = Pokemon.objects.create(
            national_dex_number=152,
            name="Chikorita",
            slug="chikorita",
        )

        PokemonGenerationData.objects.create(
            pokemon=bulbasaur,
            generation=1,
            version_group=PokemonGenerationData.VersionGroup.RED_BLUE,
            catch_rate=45,
            sprite_url="https://example.com/bulbasaur-gen1.png",
        )
        PokemonGenerationData.objects.create(
            pokemon=bulbasaur,
            generation=2,
            version_group=PokemonGenerationData.VersionGroup.GOLD_SILVER,
            catch_rate=45,
            sprite_url="https://example.com/bulbasaur-gs.png",
        )
        PokemonGenerationData.objects.create(
            pokemon=bulbasaur,
            generation=2,
            version_group=PokemonGenerationData.VersionGroup.CRYSTAL,
            catch_rate=45,
            sprite_url="https://example.com/bulbasaur-crystal.png",
        )
        PokemonGenerationData.objects.create(
            pokemon=chikorita,
            generation=2,
            version_group=PokemonGenerationData.VersionGroup.GOLD_SILVER,
            catch_rate=45,
            sprite_url="https://example.com/chikorita-gs.png",
        )
        PokemonGenerationData.objects.create(
            pokemon=chikorita,
            generation=2,
            version_group=PokemonGenerationData.VersionGroup.CRYSTAL,
            catch_rate=45,
            sprite_url="https://example.com/chikorita-crystal.png",
        )

    def test_lists_generation_one_by_default(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Bulbasaur")
        self.assertEqual(
            response.data["results"][0]["generation_data"],
            [
                {
                    "generation": 1,
                    "version_group": "red-blue",
                    "catch_rate": 45,
                    "sprite_url": "https://example.com/bulbasaur-gen1.png",
                }
            ],
        )

    def test_filters_list_by_generation_two(self) -> None:
        response = self.client.get(self.url, {"generation": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            [pokemon["name"] for pokemon in response.data["results"]],
            ["Bulbasaur", "Chikorita"],
        )
        self.assertEqual(
            [
                generation_data["version_group"]
                for generation_data in response.data["results"][0]["generation_data"]
            ],
            ["gold-silver", "crystal"],
        )

    def test_invalid_generation_returns_bad_request(self) -> None:
        response = self.client.get(self.url, {"generation": 99})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["generation"][0],
            "Generation 99 is not supported.",
        )

    def test_filters_list_by_generation_and_version_group(self) -> None:
        response = self.client.get(
            self.url,
            {"generation": 2, "version_group": "crystal"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            [pokemon["name"] for pokemon in response.data["results"]],
            ["Bulbasaur", "Chikorita"],
        )
        self.assertEqual(
            response.data["results"][0]["generation_data"],
            [
                {
                    "generation": 2,
                    "version_group": "crystal",
                    "catch_rate": 45,
                    "sprite_url": "https://example.com/bulbasaur-crystal.png",
                }
            ],
        )

    def test_invalid_version_group_returns_bad_request(self) -> None:
        response = self.client.get(
            self.url,
            {"generation": 2, "version_group": "red-blue"},
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["version_group"][0],
            "Version group 'red-blue' does not belong to Generation 2.",
        )
