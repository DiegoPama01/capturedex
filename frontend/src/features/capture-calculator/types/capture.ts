export type GenerationData = {
  generation: number;
  version_group: string;
  catch_rate: number;
  sprite_url: string;
};

export type Generation = 1 | 2 | 3 | 4 | 5;

export type VersionGroup =
  | "red-blue"
  | "gold-silver"
  | "crystal"
  | "ruby-sapphire"
  | "emerald"
  | "firered-leafgreen"
  | "diamond-pearl"
  | "platinum"
  | "heartgold-soulsilver"
  | "black-white"
  | "black-2-white-2";

export type Pokemon = {
  id: number;
  national_dex_number: number;
  name: string;
  slug: string;
  generation_data: GenerationData[];
};

export type PokemonListResponse = {
  count: number;
  next: string | null;
  previous: string | null;
  results: Pokemon[];
};

export type StatusCondition =
  | "none"
  | "poison"
  | "burn"
  | "paralysis"
  | "sleep"
  | "freeze";

export type BallType =
  | "poke_ball"
  | "great_ball"
  | "ultra_ball"
  | "master_ball"
  | "friend_ball"
  | "moon_ball"
  | "fast_ball"
  | "love_ball"
  | "level_ball"
  | "lure_ball"
  | "sport_ball"
  | "heavy_ball"
  | "premier_ball"
  | "nest_ball"
  | "repeat_ball"
  | "timer_ball"
  | "luxury_ball"
  | "dive_ball"
  | "net_ball"
  | "dusk_ball"
  | "heal_ball"
  | "quick_ball"
  | "cherish_ball"
  | "park_ball"
  | "dream_ball";

export type CaptureCalculationInput = {
  pokemon_id: number;
  generation: Generation;
  version_group: VersionGroup;
  max_hp: number;
  current_hp: number;
  status: StatusCondition;
  ball: BallType;
  attempts: number;
  player_pokemon_level?: number | null;
  wild_pokemon_level?: number | null;
  is_fishing_encounter?: boolean;
  is_surfing_encounter?: boolean;
  is_underwater_encounter?: boolean;
  is_dark_location?: boolean;
  has_caught_species_before?: boolean;
  is_same_species?: boolean;
  is_opposite_gender?: boolean;
  turns_elapsed?: number;
};

export type CaptureCalculationResponse = {
  pokemon: {
    id: number;
    national_dex_number: number;
    name: string;
    sprite_url: string;
    catch_rate: number;
  };
  result: {
    single_throw_probability: number;
    cumulative_probability: number;
    expected_throws: number;
    guaranteed: boolean;
  };
  calculation_details: Record<string, string | number | boolean>;
};
