from pokemon.models import PokemonGenerationData
from pokemon.management.commands._base_import_generation import (
    BaseImportGenerationCommand,
)


class Command(BaseImportGenerationCommand):
    help = "Import Generation I Pokémon from PokéAPI."
    FIRST_POKEMON = 1
    LAST_POKEMON = 151

    def handle(self, *args, **options) -> None:
        self.import_range(self.FIRST_POKEMON, self.LAST_POKEMON)

        self.stdout.write(
            self.style.SUCCESS("Successfully imported Generation I Pokémon.")
        )

    def import_pokemon(
        self,
        *,
        client,
        national_dex_number: int,
    ) -> None:
        species_data = self.get_species_data(client, national_dex_number)
        pokemon_data = self.get_pokemon_data(client, national_dex_number)
        pokemon = self.upsert_pokemon(national_dex_number, species_data)

        PokemonGenerationData.objects.update_or_create(
            pokemon=pokemon,
            generation=1,
            version_group=PokemonGenerationData.VersionGroup.RED_BLUE,
            defaults={
                "catch_rate": species_data["capture_rate"],
                "sprite_url": self.get_generation_one_sprite(pokemon_data),
            },
        )

        self.write_import_message(f"Imported #{national_dex_number:03d} {pokemon.name}")

    @staticmethod
    def get_generation_one_sprite(pokemon_data: dict) -> str:
        generation_one = (
            pokemon_data.get("sprites", {})
            .get("versions", {})
            .get("generation-i", {})
            .get("red-blue", {})
        )

        return (
            generation_one.get("front_default")
            or pokemon_data["sprites"].get("front_default")
            or ""
        )
