export type GenerationData = {
  generation: number;
  version_group: string;
  catch_rate: number;
  sprite_url: string;
};

export type VersionGroup = "red-blue" | "gold-silver" | "crystal";

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
  | "heavy_ball";

export type CaptureCalculationInput = {
  pokemon_id: number;
  generation: 1 | 2;
  version_group: VersionGroup;
  max_hp: number;
  current_hp: number;
  status: StatusCondition;
  ball: BallType;
  attempts: number;
  player_pokemon_level?: number | null;
  wild_pokemon_level?: number | null;
  is_fishing_encounter?: boolean;
  is_same_species?: boolean;
  is_opposite_gender?: boolean;
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
