from dataclasses import dataclass

from capture.domain.enums import BallType


@dataclass(frozen=True)
class BallContext:
    ball: BallType
    catch_rate: int
    player_pokemon_level: int | None = None
    wild_pokemon_level: int | None = None
    wild_pokemon_weight_kg: float | None = None
    is_fishing_encounter: bool = False
    evolves_with_moon_stone: bool = False
    is_fleeing_species: bool = False
    is_same_species: bool = False
    is_opposite_gender: bool = False
