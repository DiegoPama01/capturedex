from django.core.validators import MinValueValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon", "0002_alter_pokemongenerationdata_version_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokemon",
            name="evolves_with_moon_stone",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="pokemon",
            name="is_fleeing_species",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="pokemon",
            name="weight_kg",
            field=models.DecimalField(
                decimal_places=1,
                default=0,
                max_digits=6,
                validators=[MinValueValidator(0)],
            ),
        ),
    ]
