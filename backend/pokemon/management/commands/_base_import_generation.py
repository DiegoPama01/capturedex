from unicodedata import normalize

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pokemon.models import Pokemon


class BaseImportGenerationCommand(BaseCommand):
    user_agent = "CaptureDex/1.0"

    def build_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=settings.POKEAPI_BASE_URL,
            timeout=20.0,
            headers={"User-Agent": self.user_agent},
        )

    def get_json(self, client: httpx.Client, endpoint: str) -> dict:
        response = client.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_species_data(
        self,
        client: httpx.Client,
        national_dex_number: int,
    ) -> dict:
        return self.get_json(client, f"pokemon-species/{national_dex_number}/")

    def get_pokemon_data(
        self,
        client: httpx.Client,
        national_dex_number: int,
    ) -> dict:
        return self.get_json(client, f"pokemon/{national_dex_number}/")

    def upsert_pokemon(self, national_dex_number: int, species_data: dict) -> Pokemon:
        pokemon, _ = Pokemon.objects.update_or_create(
            national_dex_number=national_dex_number,
            defaults={
                "name": self.get_spanish_name(species_data),
                "slug": species_data["name"],
            },
        )
        return pokemon

    def import_range(self, first_pokemon: int, last_pokemon: int) -> None:
        with self.build_client() as client:
            for national_dex_number in range(first_pokemon, last_pokemon + 1):
                try:
                    self.import_pokemon(
                        client=client,
                        national_dex_number=national_dex_number,
                    )
                except httpx.HTTPError as error:
                    raise CommandError(
                        f"Could not import Pokemon #{national_dex_number}: {error}"
                    ) from error

    def write_import_message(self, message: str) -> None:
        self.stdout.write(self.safe_console_text(message))

    @staticmethod
    def get_spanish_name(species_data: dict) -> str:
        for localized_name in species_data["names"]:
            if localized_name["language"]["name"] == "es":
                return localized_name["name"]

        return species_data["name"].replace("-", " ").title()

    @staticmethod
    def safe_console_text(text: str) -> str:
        return normalize("NFKD", text).encode("cp1252", "replace").decode("cp1252")
