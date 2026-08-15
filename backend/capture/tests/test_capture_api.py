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
            version_group=(PokemonGenerationData.VersionGroup.RED_BLUE),
            catch_rate=190,
            sprite_url="https://example.com/pikachu.png",
        )

        moon_stone_pokemon = Pokemon.objects.create(
            national_dex_number=30,
            name="Nidorina",
            slug="nidorina",
            weight_kg=20,
            evolves_with_moon_stone=True,
        )

        PokemonGenerationData.objects.create(
            pokemon=moon_stone_pokemon,
            generation=2,
            version_group=(PokemonGenerationData.VersionGroup.GOLD_SILVER),
            catch_rate=120,
            sprite_url="https://example.com/nidorina.png",
        )

        heavy_ball_pokemon = Pokemon.objects.create(
            national_dex_number=143,
            name="Snorlax",
            slug="snorlax",
            weight_kg=460,
        )

        PokemonGenerationData.objects.create(
            pokemon=heavy_ball_pokemon,
            generation=2,
            version_group=(PokemonGenerationData.VersionGroup.GOLD_SILVER),
            catch_rate=25,
            sprite_url="https://example.com/snorlax.png",
        )

        fast_ball_pokemon = Pokemon.objects.create(
            national_dex_number=81,
            name="Magnemite",
            slug="magnemite",
            weight_kg=6,
            is_fleeing_species=True,
        )

        PokemonGenerationData.objects.create(
            pokemon=fast_ball_pokemon,
            generation=2,
            version_group=(PokemonGenerationData.VersionGroup.GOLD_SILVER),
            catch_rate=190,
            sprite_url="https://example.com/magnemite.png",
        )

        wingull = Pokemon.objects.create(
            national_dex_number=278,
            name="Wingull",
            slug="wingull",
            weight_kg=9.5,
            types=["water", "flying"],
        )

        PokemonGenerationData.objects.create(
            pokemon=wingull,
            generation=3,
            version_group=(PokemonGenerationData.VersionGroup.RUBY_SAPPHIRE),
            catch_rate=190,
            sprite_url="https://example.com/wingull-rs.png",
        )

        zubat = Pokemon.objects.create(
            national_dex_number=41,
            name="Zubat",
            slug="zubat",
            weight_kg=7.5,
        )

        PokemonGenerationData.objects.create(
            pokemon=zubat,
            generation=4,
            version_group=(PokemonGenerationData.VersionGroup.DIAMOND_PEARL),
            catch_rate=255,
            sprite_url="https://example.com/zubat-dp.png",
        )

        munna = Pokemon.objects.create(
            national_dex_number=517,
            name="Munna",
            slug="munna",
            weight_kg=23.3,
        )

        PokemonGenerationData.objects.create(
            pokemon=munna,
            generation=5,
            version_group=(PokemonGenerationData.VersionGroup.BLACK_WHITE),
            catch_rate=190,
            sprite_url="https://example.com/munna-bw.png",
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

    def test_uses_moon_stone_metadata_automatically(self) -> None:
        payload = {
            "pokemon_id": Pokemon.objects.get(slug="nidorina").id,
            "generation": 2,
            "version_group": "gold-silver",
            "max_hp": 100,
            "current_hp": 100,
            "status": "none",
            "ball": "moon_ball",
            "attempts": 1,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["calculation_details"]["modified_catch_rate"],
            255,
        )

    def test_uses_heavy_ball_weight_metadata_automatically(self) -> None:
        payload = {
            "pokemon_id": Pokemon.objects.get(slug="snorlax").id,
            "generation": 2,
            "version_group": "gold-silver",
            "max_hp": 100,
            "current_hp": 100,
            "status": "none",
            "ball": "heavy_ball",
            "attempts": 1,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["calculation_details"]["modified_catch_rate"],
            65,
        )

    def test_uses_fast_ball_species_metadata_automatically(self) -> None:
        payload = {
            "pokemon_id": Pokemon.objects.get(slug="magnemite").id,
            "generation": 2,
            "version_group": "gold-silver",
            "max_hp": 100,
            "current_hp": 100,
            "status": "none",
            "ball": "fast_ball",
            "attempts": 1,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["calculation_details"]["modified_catch_rate"],
            255,
        )

    def test_generation_three_uses_default_version_group(self) -> None:
        payload = {
            "pokemon_id": Pokemon.objects.get(slug="wingull").id,
            "generation": 3,
            "max_hp": 100,
            "current_hp": 100,
            "status": "none",
            "ball": "dive_ball",
            "is_surfing_encounter": True,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["calculation_details"]["modified_catch_rate"],
            255,
        )

    def test_generation_three_uses_type_metadata_automatically(self) -> None:
        payload = {
            "pokemon_id": Pokemon.objects.get(slug="wingull").id,
            "generation": 3,
            "version_group": "ruby-sapphire",
            "max_hp": 100,
            "current_hp": 100,
            "status": "none",
            "ball": "net_ball",
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["calculation_details"]["modified_catch_rate"],
            255,
        )

    def test_generation_four_dusk_ball_uses_dark_location_flag(self) -> None:
        payload = {
            "pokemon_id": Pokemon.objects.get(slug="zubat").id,
            "generation": 4,
            "version_group": "diamond-pearl",
            "max_hp": 100,
            "current_hp": 100,
            "status": "none",
            "ball": "dusk_ball",
            "is_dark_location": True,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["calculation_details"]["modified_catch_rate"],
            255,
        )

    def test_generation_five_dream_ball_matches_poke_ball_outside_park(self) -> None:
        payload = {
            "pokemon_id": Pokemon.objects.get(slug="munna").id,
            "generation": 5,
            "version_group": "black-white",
            "max_hp": 100,
            "current_hp": 100,
            "status": "sleep",
            "ball": "dream_ball",
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["calculation_details"]["modified_catch_rate"],
            190,
        )
