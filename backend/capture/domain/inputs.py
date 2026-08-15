from dataclasses import dataclass

from .enums import BallType, StatusCondition


@dataclass(frozen=True)
class CaptureInput:
    generation: int
    catch_rate: int
    max_hp: int
    current_hp: int
    status: StatusCondition
    ball: BallType
    attempts: int = 1
    player_pokemon_level: int | None = None
    wild_pokemon_level: int | None = None
    wild_pokemon_weight_kg: float | None = None
    is_fishing_encounter: bool = False
    evolves_with_moon_stone: bool = False
    is_fleeing_species: bool = False
    is_same_species: bool = False
    is_opposite_gender: bool = False

    SUPPORTED_GENERATIONS = (1, 2)

    def __post_init__(self) -> None:
        if self.generation not in self.SUPPORTED_GENERATIONS:
            raise ValueError("Only Generations I and II are currently supported.")

        if not 1 <= self.catch_rate <= 255:
            raise ValueError("Catch rate must be between 1 and 255.")

        if not 1 <= self.max_hp <= 999:
            raise ValueError("Maximum HP must be between 1 and 999.")

        if not 1 <= self.current_hp <= self.max_hp:
            raise ValueError("Current HP must be between 1 and maximum HP.")

        if not 1 <= self.attempts <= 1000:
            raise ValueError("Attempts must be between 1 and 1000.")

        if (
            self.player_pokemon_level is not None
            and not 1 <= self.player_pokemon_level <= 100
        ):
            raise ValueError("Player Pokemon level must be between 1 and 100.")

        if (
            self.wild_pokemon_level is not None
            and not 1 <= self.wild_pokemon_level <= 100
        ):
            raise ValueError("Wild Pokemon level must be between 1 and 100.")

        if self.wild_pokemon_weight_kg is not None and self.wild_pokemon_weight_kg < 0:
            raise ValueError("Wild Pokemon weight must be greater than or equal to 0.")
