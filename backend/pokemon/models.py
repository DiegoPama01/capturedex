from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Pokemon(models.Model):
    national_dex_number = models.PositiveSmallIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1025),
        ],
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        default=0,
        validators=[MinValueValidator(0)],
    )
    base_speed = models.PositiveSmallIntegerField(default=0)
    types = models.JSONField(default=list, blank=True)
    evolves_with_moon_stone = models.BooleanField(default=False)
    is_fleeing_species = models.BooleanField(default=False)

    class Meta:
        ordering = ["national_dex_number"]
        verbose_name = "Pokémon"
        verbose_name_plural = "Pokémon"

    def __str__(self) -> str:
        return f"#{self.national_dex_number:04d} {self.name}"


class PokemonGenerationData(models.Model):
    class VersionGroup(models.TextChoices):
        RED_BLUE = "red-blue", "Red/Blue"
        GOLD_SILVER = "gold-silver", "Gold/Silver"
        CRYSTAL = "crystal", "Crystal"
        RUBY_SAPPHIRE = "ruby-sapphire", "Ruby/Sapphire"
        EMERALD = "emerald", "Emerald"
        FIRERED_LEAFGREEN = "firered-leafgreen", "FireRed/LeafGreen"
        DIAMOND_PEARL = "diamond-pearl", "Diamond/Pearl"
        PLATINUM = "platinum", "Platinum"
        HEARTGOLD_SOULSILVER = "heartgold-soulsilver", "HeartGold/SoulSilver"
        BLACK_WHITE = "black-white", "Black/White"
        BLACK_2_WHITE_2 = "black-2-white-2", "Black 2/White 2"

    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="generation_data",
    )
    generation = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(9),
        ],
    )
    version_group = models.CharField(
        max_length=30,
        choices=VersionGroup.choices,
    )
    catch_rate = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(255),
        ],
    )
    sprite_url = models.URLField(blank=True)

    class Meta:
        ordering = [
            "generation",
            "pokemon__national_dex_number",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "pokemon",
                    "generation",
                    "version_group",
                ],
                name="unique_pokemon_generation_version",
            ),
        ]
        verbose_name = "Pokémon generation data"
        verbose_name_plural = "Pokémon generation data"

    def __str__(self) -> str:
        return (
            f"{self.pokemon.name} · "
            f"Generation {self.generation} · "
            f"{self.get_version_group_display()}"
        )
