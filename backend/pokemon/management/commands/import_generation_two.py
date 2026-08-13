from pokemon.models import PokemonGenerationData
from pokemon.management.commands._base_import_generation import (
    BaseImportGenerationCommand,
)


class Command(BaseImportGenerationCommand):
    help = "Import Generation II Pokémon data from PokéAPI."

    FIRST_POKEMON = 1
    LAST_POKEMON = 251

    VERSION_GROUPS = (
        PokemonGenerationData.VersionGroup.GOLD_SILVER,
        PokemonGenerationData.VersionGroup.CRYSTAL,
    )

    def handle(self, *args, **options) -> None:
        self.import_range(self.FIRST_POKEMON, self.LAST_POKEMON)

        self.stdout.write(
            self.style.SUCCESS("Successfully imported Generation II data.")
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

        sprites = (
            pokemon_data.get("sprites", {}).get("versions", {}).get("generation-ii", {})
        )

        version_sprites = {
            PokemonGenerationData.VersionGroup.GOLD_SILVER: (
                sprites.get("gold", {}).get("front_default")
                or sprites.get("silver", {}).get("front_default")
                or ""
            ),
            PokemonGenerationData.VersionGroup.CRYSTAL: (
                sprites.get("crystal", {}).get("front_default") or ""
            ),
        }

        for version_group in self.VERSION_GROUPS:
            PokemonGenerationData.objects.update_or_create(
                pokemon=pokemon,
                generation=2,
                version_group=version_group,
                defaults={
                    "catch_rate": species_data["capture_rate"],
                    "sprite_url": version_sprites[version_group],
                },
            )

        self.write_import_message(
            f"Imported Gen II data for #{national_dex_number:03d} {pokemon.name}"
        )
