from unicodedata import normalize
from abc import abstractmethod

import httpx
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pokemon.models import Pokemon


class BaseImportGenerationCommand(BaseCommand):
    user_agent = "CaptureDex/1.0"
    FLEEING_SPECIES = frozenset(
        {
            "magnemite",
            "grimer",
            "tangela",
        }
    )

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

    def get_evolution_chain_data(
        self,
        client: httpx.Client,
        species_data: dict,
    ) -> dict:
        evolution_chain_url = species_data["evolution_chain"]["url"]
        endpoint = evolution_chain_url.removeprefix(settings.POKEAPI_BASE_URL)
        return self.get_json(client, endpoint)

    def upsert_pokemon(
        self,
        national_dex_number: int,
        species_data: dict,
        pokemon_data: dict,
        evolution_chain_data: dict,
    ) -> Pokemon:
        pokemon, _ = Pokemon.objects.update_or_create(
            national_dex_number=national_dex_number,
            defaults={
                "name": self.get_spanish_name(species_data),
                "slug": species_data["name"],
                "weight_kg": self.get_weight_kg(pokemon_data),
                "base_speed": self.get_base_speed(pokemon_data),
                "types": self.get_types(pokemon_data),
                "is_ultra_beast": self.is_ultra_beast(species_data),
                "evolves_with_moon_stone": self.evolves_with_moon_stone(
                    species_data,
                    evolution_chain_data,
                ),
                "is_fleeing_species": self.is_fleeing_species(species_data),
            },
        )
        return pokemon

    @staticmethod
    def get_weight_kg(pokemon_data: dict) -> float:
        return pokemon_data.get("weight", 0) / 10

    @staticmethod
    def get_base_speed(pokemon_data: dict) -> int:
        for stat_entry in pokemon_data.get("stats", []):
            if stat_entry.get("stat", {}).get("name") == "speed":
                return stat_entry.get("base_stat", 0)

        return 0

    @staticmethod
    def get_types(pokemon_data: dict) -> list[str]:
        return [
            pokemon_type.get("type", {}).get("name")
            for pokemon_type in sorted(
                pokemon_data.get("types", []),
                key=lambda pokemon_type: pokemon_type.get("slot", 0),
            )
            if pokemon_type.get("type", {}).get("name")
        ]

    @staticmethod
    def is_ultra_beast(species_data: dict) -> bool:
        return species_data.get("is_legendary") is False and (
            species_data.get("generation", {}).get("name") == "generation-vii"
            and species_data.get("capture_rate") == 45
            and species_data.get("is_mythical") is False
            and species_data.get("name")
            in {
                "nihilego",
                "buzzwole",
                "pheromosa",
                "xurkitree",
                "celesteela",
                "kartana",
                "guzzlord",
                "poipole",
                "naganadel",
                "stakataka",
                "blacephalon",
            }
        )

    @staticmethod
    def evolves_with_moon_stone(
        species_data: dict,
        evolution_chain_data: dict,
    ) -> bool:
        species_name = species_data["name"]
        chain = evolution_chain_data.get("chain", {})

        def walks_into_moon_stone_evolution(node: dict) -> bool:
            if node.get("species", {}).get("name") == species_name:
                for next_evolution in node.get("evolves_to", []):
                    for detail in next_evolution.get(
                        "evolution_details",
                        [],
                    ):
                        item = detail.get("item")
                        if item and item.get("name") == "moon-stone":
                            return True

            return any(
                walks_into_moon_stone_evolution(next_evolution)
                for next_evolution in node.get("evolves_to", [])
            )

        return walks_into_moon_stone_evolution(chain)

    @classmethod
    def is_fleeing_species(cls, species_data: dict) -> bool:
        return species_data["name"] in cls.FLEEING_SPECIES

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

    @abstractmethod
    def import_pokemon(
        self,
        *,
        client: httpx.Client,
        national_dex_number: int,
    ) -> None:
        raise NotImplementedError

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
