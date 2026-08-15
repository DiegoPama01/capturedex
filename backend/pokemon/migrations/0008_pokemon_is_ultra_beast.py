from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon", "0007_alter_pokemongenerationdata_version_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokemon",
            name="is_ultra_beast",
            field=models.BooleanField(default=False),
        ),
    ]
