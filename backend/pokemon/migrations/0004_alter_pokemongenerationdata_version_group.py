from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon", "0003_pokemon_ball_metadata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemongenerationdata",
            name="version_group",
            field=models.CharField(
                choices=[
                    ("red-blue", "Red/Blue"),
                    ("gold-silver", "Gold/Silver"),
                    ("crystal", "Crystal"),
                    ("ruby-sapphire", "Ruby/Sapphire"),
                    ("emerald", "Emerald"),
                    ("firered-leafgreen", "FireRed/LeafGreen"),
                    ("diamond-pearl", "Diamond/Pearl"),
                    ("platinum", "Platinum"),
                    ("heartgold-soulsilver", "HeartGold/SoulSilver"),
                    ("black-white", "Black/White"),
                    ("black-2-white-2", "Black 2/White 2"),
                ],
                max_length=30,
            ),
        ),
    ]
