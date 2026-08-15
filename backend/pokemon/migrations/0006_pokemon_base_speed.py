from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon", "0005_pokemon_types"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokemon",
            name="base_speed",
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
