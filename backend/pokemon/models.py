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

    class Meta:
        ordering = ["national_dex_number"]
        verbose_name = "Pokémon"
        verbose_name_plural = "Pokémon"

    def __str__(self) -> str:
        return f"#{self.national_dex_number:04d} {self.name}"


class PokemonGenerationData(models.Model):
    class VersionGroup(models.TextChoices):
        RED_BLUE = "red-blue", "Red/Blue"

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