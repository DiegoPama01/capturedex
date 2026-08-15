from pokemon.management.commands._base_import_generation import (
    BaseImportGenerationCommand,
)
from pokemon.models import PokemonGenerationData


class Command(BaseImportGenerationCommand):
    help = "Import Generation IX Pokemon data from PokeAPI."

    FIRST_POKEMON = 1
    LAST_POKEMON = 1025
    VERSION_GROUPS = (PokemonGenerationData.VersionGroup.SCARLET_VIOLET,)

    def handle(self, *args, **options) -> None:
        self.import_range(self.FIRST_POKEMON, self.LAST_POKEMON)
        self.stdout.write(
            self.style.SUCCESS("Successfully imported Generation IX data.")
        )

    def import_pokemon(self, *, client, national_dex_number: int) -> None:
        species_data = self.get_species_data(client, national_dex_number)
        pokemon_data = self.get_pokemon_data(client, national_dex_number)
        evolution_chain_data = self.get_evolution_chain_data(client, species_data)
        pokemon = self.upsert_pokemon(
            national_dex_number, species_data, pokemon_data, evolution_chain_data
        )

        sprite = pokemon_data.get("sprites", {}).get("front_default") or ""
        PokemonGenerationData.objects.update_or_create(
            pokemon=pokemon,
            generation=9,
            version_group=PokemonGenerationData.VersionGroup.SCARLET_VIOLET,
            defaults={"catch_rate": species_data["capture_rate"], "sprite_url": sprite},
        )

        self.write_import_message(
            f"Imported Gen IX data for #{national_dex_number:03d} {pokemon.name}"
        )
