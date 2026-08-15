from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import Pokemon data for Generations I to IX."

    COMMANDS = (
        ("import_generation_one", "Generation I"),
        ("import_generation_two", "Generation II"),
        ("import_generation_three", "Generation III"),
        ("import_generation_four", "Generation IV"),
        ("import_generation_five", "Generation V"),
        ("import_generation_six", "Generation VI"),
        ("import_generation_seven", "Generation VII"),
        ("import_generation_eight", "Generation VIII"),
        ("import_generation_nine", "Generation IX"),
    )

    def handle(self, *args, **options) -> None:
        for command_name, label in self.COMMANDS:
            self.stdout.write(f"Starting {label} import...")
            call_command(command_name)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully imported Pokemon data for Generations I to IX."
            )
        )
