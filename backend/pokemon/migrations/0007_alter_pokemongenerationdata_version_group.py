from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon", "0006_pokemon_base_speed"),
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
                    ("x-y", "X/Y"),
                    ("omega-ruby-alpha-sapphire", "Omega Ruby/Alpha Sapphire"),
                    ("sun-moon", "Sun/Moon"),
                    ("ultra-sun-ultra-moon", "Ultra Sun/Ultra Moon"),
                    (
                        "lets-go-pikachu-lets-go-eevee",
                        "Let's Go Pikachu/Let's Go Eevee",
                    ),
                    ("sword-shield", "Sword/Shield"),
                    (
                        "brilliant-diamond-shining-pearl",
                        "Brilliant Diamond/Shining Pearl",
                    ),
                    ("legends-arceus", "Legends: Arceus"),
                    ("scarlet-violet", "Scarlet/Violet"),
                ],
                max_length=40,
            ),
        ),
    ]
