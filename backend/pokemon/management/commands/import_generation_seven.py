from pokemon.management.commands._base_import_generation import (
    BaseImportGenerationCommand,
)
from pokemon.models import PokemonGenerationData


class Command(BaseImportGenerationCommand):
    help = "Import Generation VII Pokemon data from PokeAPI."

    FIRST_POKEMON = 1
    LAST_POKEMON = 809
    VERSION_GROUPS = (
        PokemonGenerationData.VersionGroup.SUN_MOON,
        PokemonGenerationData.VersionGroup.ULTRA_SUN_ULTRA_MOON,
        PokemonGenerationData.VersionGroup.LETS_GO_PIKACHU_LETS_GO_EEVEE,
    )

    def handle(self, *args, **options) -> None:
        self.import_range(self.FIRST_POKEMON, self.LAST_POKEMON)
        self.stdout.write(
            self.style.SUCCESS("Successfully imported Generation VII data.")
        )

    def import_pokemon(self, *, client, national_dex_number: int) -> None:
        species_data = self.get_species_data(client, national_dex_number)
        pokemon_data = self.get_pokemon_data(client, national_dex_number)
        evolution_chain_data = self.get_evolution_chain_data(client, species_data)
        pokemon = self.upsert_pokemon(
            national_dex_number, species_data, pokemon_data, evolution_chain_data
        )

        sprites = (
            pokemon_data.get("sprites", {})
            .get("versions", {})
            .get("generation-vii", {})
        )
        version_sprites = {
            PokemonGenerationData.VersionGroup.SUN_MOON: sprites.get("icons", {}).get(
                "front_default"
            )
            or "",
            PokemonGenerationData.VersionGroup.ULTRA_SUN_ULTRA_MOON: sprites.get(
                "ultra-sun-ultra-moon", {}
            ).get("front_default")
            or "",
            PokemonGenerationData.VersionGroup.LETS_GO_PIKACHU_LETS_GO_EEVEE: sprites.get(
                "icons", {}
            ).get("front_default")
            or "",
        }

        for version_group in self.VERSION_GROUPS:
            PokemonGenerationData.objects.update_or_create(
                pokemon=pokemon,
                generation=7,
                version_group=version_group,
                defaults={
                    "catch_rate": species_data["capture_rate"],
                    "sprite_url": version_sprites[version_group],
                },
            )

        self.write_import_message(
            f"Imported Gen VII data for #{national_dex_number:03d} {pokemon.name}"
        )
