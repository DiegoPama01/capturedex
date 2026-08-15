from dataclasses import dataclass

from capture.domain.enums import BallType


@dataclass(frozen=True)
class BallContext:
    ball: BallType
    catch_rate: int
    status: str | None = None
    player_pokemon_level: int | None = None
    wild_pokemon_level: int | None = None
    wild_pokemon_weight_kg: float | None = None
    wild_pokemon_base_speed: int | None = None
    is_fishing_encounter: bool = False
    is_surfing_encounter: bool = False
    is_underwater_encounter: bool = False
    is_dark_location: bool = False
    has_caught_species_before: bool = False
    is_water_type: bool = False
    is_bug_type: bool = False
    evolves_with_moon_stone: bool = False
    is_fleeing_species: bool = False
    is_same_species: bool = False
    is_opposite_gender: bool = False
    turns_elapsed: int = 1
