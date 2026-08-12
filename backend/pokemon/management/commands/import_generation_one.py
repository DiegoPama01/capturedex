import httpx
from django.core.management.base import BaseCommand, CommandError

from pokemon.models import Pokemon, PokemonGenerationData


class Command(BaseCommand):
    help = "Import Generation I Pokémon from PokéAPI."

    API_URL = "https://pokeapi.co/api/v2/"

    def handle(self, *args, **options) -> None:
        with httpx.Client(
            base_url=self.API_URL,
            timeout=20.0,
            headers={
                "User-Agent": "CaptureDex/1.0",
            },
        ) as client:
            for national_dex_number in range(1, 152):
                try:
                    self._import_pokemon(
                        client=client,
                        national_dex_number=national_dex_number,
                    )
                except httpx.HTTPError as error:
                    raise CommandError(
                        f"Could not import Pokémon "
                        f"#{national_dex_number}: {error}"
                    ) from error

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully imported Generation I Pokémon."
            )
        )

    def _import_pokemon(
        self,
        *,
        client: httpx.Client,
        national_dex_number: int,
    ) -> None:
        species_response = client.get(
            f"pokemon-species/{national_dex_number}/"
        )
        species_response.raise_for_status()
        species_data = species_response.json()

        pokemon_response = client.get(
            f"pokemon/{national_dex_number}/"
        )
        pokemon_response.raise_for_status()
        pokemon_data = pokemon_response.json()

        pokemon, _ = Pokemon.objects.update_or_create(
            national_dex_number=national_dex_number,
            defaults={
                "name": self._get_spanish_name(species_data),
                "slug": species_data["name"],
            },
        )

        PokemonGenerationData.objects.update_or_create(
            pokemon=pokemon,
            generation=1,
            version_group=(
                PokemonGenerationData.VersionGroup.RED_BLUE
            ),
            defaults={
                "catch_rate": species_data["capture_rate"],
                "sprite_url": self._get_generation_one_sprite(
                    pokemon_data
                ),
            },
        )

        self.stdout.write(
            f"Imported #{national_dex_number:03d} {pokemon.name}"
        )

    @staticmethod
    def _get_spanish_name(species_data: dict) -> str:
        for localized_name in species_data["names"]:
            if localized_name["language"]["name"] == "es":
                return localized_name["name"]

        return species_data["name"].replace("-", " ").title()

    @staticmethod
    def _get_generation_one_sprite(pokemon_data: dict) -> str:
        generation_one = (
            pokemon_data
            .get("sprites", {})
            .get("versions", {})
            .get("generation-i", {})
            .get("red-blue", {})
        )

        return (
            generation_one.get("front_default")
            or pokemon_data["sprites"].get("front_default")
            or ""
        )