from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon", "0004_alter_pokemongenerationdata_version_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokemon",
            name="types",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
