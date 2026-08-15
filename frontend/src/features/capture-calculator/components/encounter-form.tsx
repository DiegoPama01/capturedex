"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type {
  BallType,
  CaptureCalculationInput,
  Generation,
  Pokemon,
  StatusCondition,
  VersionGroup,
} from "@/features/capture-calculator/types/capture";
import { PokemonCombobox } from "./pokemon-combobox";
import {
  PokeballCombobox,
  type PokeballOption,
} from "./pokeball-combobox";

type EncounterFormProps = {
  pokemon: Pokemon[];
  generation: Generation;
  versionGroup: VersionGroup;
  attempts: number;
  isSubmitting: boolean;
  isLoadingPokemon: boolean;
  isLoadingMorePokemon: boolean;
  hasMorePokemon: boolean;
  error: string | null;
  initialValues?: CaptureCalculationInput;
  onVersionGroupChange: (versionGroup: VersionGroup) => void;
  onPokemonSearchChange: (search: string) => void;
  onLoadMorePokemon: () => Promise<void> | void;
  onSubmit: (input: CaptureCalculationInput) => Promise<void> | void;
};

const versionGroupOptions: Array<{
  value: VersionGroup;
  label: string;
  generation: Generation;
}> = [
  { value: "red-blue", label: "Red / Blue", generation: 1 },
  { value: "gold-silver", label: "Gold / Silver", generation: 2 },
  { value: "crystal", label: "Crystal", generation: 2 },
  { value: "ruby-sapphire", label: "Ruby / Sapphire", generation: 3 },
  { value: "emerald", label: "Emerald", generation: 3 },
  {
    value: "firered-leafgreen",
    label: "FireRed / LeafGreen",
    generation: 3,
  },
  { value: "diamond-pearl", label: "Diamond / Pearl", generation: 4 },
  { value: "platinum", label: "Platinum", generation: 4 },
  {
    value: "heartgold-soulsilver",
    label: "HeartGold / SoulSilver",
    generation: 4,
  },
  { value: "black-white", label: "Black / White", generation: 5 },
  {
    value: "black-2-white-2",
    label: "Black 2 / White 2",
    generation: 5,
  },
  { value: "x-y", label: "X / Y", generation: 6 },
  {
    value: "omega-ruby-alpha-sapphire",
    label: "Omega Ruby / Alpha Sapphire",
    generation: 6,
  },
  { value: "sun-moon", label: "Sun / Moon", generation: 7 },
  {
    value: "ultra-sun-ultra-moon",
    label: "Ultra Sun / Ultra Moon",
    generation: 7,
  },
  {
    value: "lets-go-pikachu-lets-go-eevee",
    label: "Let's Go Pikachu / Let's Go Eevee",
    generation: 7,
  },
  { value: "sword-shield", label: "Sword / Shield", generation: 8 },
  {
    value: "brilliant-diamond-shining-pearl",
    label: "Brilliant Diamond / Shining Pearl",
    generation: 8,
  },
  { value: "legends-arceus", label: "Legends: Arceus", generation: 8 },
  { value: "scarlet-violet", label: "Scarlet / Violet", generation: 9 },
];

const statusOptions: Array<{
  value: StatusCondition;
  label: string;
}> = [
  { value: "none", label: "Sin estado" },
  { value: "poison", label: "Envenenado" },
  { value: "burn", label: "Quemado" },
  { value: "paralysis", label: "Paralizado" },
  { value: "sleep", label: "Dormido" },
  { value: "freeze", label: "Congelado" },
];

const baseBallOptions: PokeballOption[] = [
  { value: "poke_ball", label: "Poke Ball", sprite: "/pokeballs/Poké_Ball.png" },
  { value: "great_ball", label: "Great Ball", sprite: "/pokeballs/Super_Ball.png" },
  { value: "ultra_ball", label: "Ultra Ball", sprite: "/pokeballs/Ultra_Ball.png" },
  { value: "master_ball", label: "Master Ball", sprite: "/pokeballs/Master_Ball.png" },
];

const generationTwoOnlyBallOptions: PokeballOption[] = [
  { value: "friend_ball", label: "Amigo Ball", sprite: "/pokeballs/Amigo_Ball.png" },
  { value: "moon_ball", label: "Luna Ball", sprite: "/pokeballs/Luna_Ball.png" },
  { value: "fast_ball", label: "Rapid Ball", sprite: "/pokeballs/Rapid_Ball.png" },
  { value: "love_ball", label: "Amor Ball", sprite: "/pokeballs/Amor_Ball.png" },
  { value: "level_ball", label: "Nivel Ball", sprite: "/pokeballs/Nivel_Ball.png" },
  { value: "lure_ball", label: "Cebo Ball", sprite: "/pokeballs/Cebo_Ball.png" },
  { value: "sport_ball", label: "Competi Ball", sprite: "/pokeballs/Competi_Ball.png" },
  { value: "heavy_ball", label: "Peso Ball", sprite: "/pokeballs/Peso_Ball.png" },
];

const generationThreePlusBallOptions: PokeballOption[] = [
  { value: "premier_ball", label: "Honor Ball", sprite: "/pokeballs/Honor_Ball.png" },
  { value: "nest_ball", label: "Nido Ball", sprite: "/pokeballs/Nido_Ball.png" },
  { value: "repeat_ball", label: "Acopio Ball", sprite: "/pokeballs/Acopio_Ball.png" },
  { value: "timer_ball", label: "Turno Ball", sprite: "/pokeballs/Turno_Ball.png" },
  { value: "luxury_ball", label: "Lujo Ball", sprite: "/pokeballs/Lujo_Ball.png" },
  { value: "dive_ball", label: "Buceo Ball", sprite: "/pokeballs/Buceo_Ball.png" },
  { value: "net_ball", label: "Malla Ball", sprite: "/pokeballs/Malla_Ball.png" },
];

const generationFourOnlyBallOptions: PokeballOption[] = [
  { value: "dusk_ball", label: "Ocaso Ball", sprite: "/pokeballs/Ocaso_Ball.png" },
  { value: "heal_ball", label: "Sana Ball", sprite: "/pokeballs/Sana_Ball.png" },
  { value: "quick_ball", label: "Veloz Ball", sprite: "/pokeballs/Veloz_Ball.png" },
  { value: "cherish_ball", label: "Gloria Ball", sprite: "/pokeballs/Gloria_Ball.png" },
  { value: "park_ball", label: "Parque Ball", sprite: "/pokeballs/Parque_Ball.png" },
];

const generationFiveOnlyBallOptions: PokeballOption[] = [
  { value: "dream_ball", label: "Ensueno Ball", sprite: "/pokeballs/Ensueño_Ball.png" },
];

const generationSevenOnlyBallOptions: PokeballOption[] = [
  { value: "beast_ball", label: "Ente Ball", sprite: "/pokeballs/Ente_Ball.png" },
];

const generationEightOnlyBallOptions: PokeballOption[] = [
  { value: "beast_ball", label: "Ente Ball", sprite: "/pokeballs/Ente_Ball.png" },
];

const legendsArceusBallOptions: PokeballOption[] = [
  { value: "feather_ball", label: "Pluma Ball", sprite: "/pokeballs/Pluma_Ball.png" },
  { value: "wing_ball", label: "Ala Ball", sprite: "/pokeballs/Ala_Ball.png" },
  { value: "jet_ball", label: "Aero Ball", sprite: "/pokeballs/Aero_Ball.png" },
  {
    value: "hisui_heavy_ball",
    label: "Peso Ball de Hisui",
    sprite: "/pokeballs/Peso_Ball_(Hisui).png",
  },
  { value: "leaden_ball", label: "Kilo Ball", sprite: "/pokeballs/Kilo_Ball.png" },
  { value: "gigaton_ball", label: "Quintal Ball", sprite: "/pokeballs/Quintal_Ball.png" },
  { value: "origin_ball", label: "Origen Ball", sprite: "/pokeballs/Origen_Ball.png" },
  { value: "strange_ball", label: "Extrana Ball", sprite: "/pokeballs/Extraña_Ball.png" },
];

const ballOptionsByGeneration: Record<Generation, PokeballOption[]> = {
  1: baseBallOptions,
  2: [...baseBallOptions, ...generationTwoOnlyBallOptions],
  3: [...baseBallOptions, ...generationThreePlusBallOptions],
  4: [
    ...baseBallOptions,
    ...generationTwoOnlyBallOptions,
    ...generationThreePlusBallOptions,
    ...generationFourOnlyBallOptions,
  ],
  5: [
    ...baseBallOptions,
    ...generationTwoOnlyBallOptions,
    ...generationThreePlusBallOptions,
    ...generationFourOnlyBallOptions,
    ...generationFiveOnlyBallOptions,
  ],
  6: [
    ...baseBallOptions,
    ...generationTwoOnlyBallOptions,
    ...generationThreePlusBallOptions,
    ...generationFourOnlyBallOptions,
    ...generationFiveOnlyBallOptions,
  ],
  7: [
    ...baseBallOptions,
    ...generationTwoOnlyBallOptions,
    ...generationThreePlusBallOptions,
    ...generationFourOnlyBallOptions,
    ...generationFiveOnlyBallOptions,
    ...generationSevenOnlyBallOptions,
  ],
  8: [
    ...baseBallOptions,
    ...generationTwoOnlyBallOptions,
    ...generationThreePlusBallOptions,
    ...generationFourOnlyBallOptions,
    ...generationFiveOnlyBallOptions,
    ...generationSevenOnlyBallOptions,
    ...generationEightOnlyBallOptions,
  ],
  9: [
    ...baseBallOptions,
    ...generationTwoOnlyBallOptions,
    ...generationThreePlusBallOptions,
    ...generationFourOnlyBallOptions,
    ...generationFiveOnlyBallOptions,
    ...generationSevenOnlyBallOptions,
    ...generationEightOnlyBallOptions,
  ],
};

const ballOptionsByVersionGroup: Partial<Record<VersionGroup, PokeballOption[]>> = {
  "legends-arceus": legendsArceusBallOptions,
};

const ballContextFieldsByBall: Partial<Record<BallType, string[]>> = {
  love_ball: ["is_same_species", "is_opposite_gender"],
  level_ball: ["player_pokemon_level", "wild_pokemon_level"],
  lure_ball: ["is_fishing_encounter"],
  net_ball: [],
  dive_ball: ["is_fishing_encounter", "is_surfing_encounter", "is_underwater_encounter"],
  nest_ball: ["wild_pokemon_level"],
  repeat_ball: ["has_caught_species_before"],
  timer_ball: ["turns_elapsed"],
  dusk_ball: ["is_dark_location"],
  quick_ball: ["turns_elapsed"],
};

function getOptionLabel<T extends string>(
  options: Array<{ value: T; label: string }>,
  value: T,
) {
  return options.find((option) => option.value === value)?.label ?? value;
}

const versionGroupsByGeneration = versionGroupOptions.reduce<
  Record<Generation, Array<{ value: VersionGroup; label: string }>>
>(
  (groups, option) => {
    groups[option.generation].push({
      value: option.value,
      label: option.label,
    });
    return groups;
  },
  {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
  },
);

export function EncounterForm({
  pokemon,
  generation,
  versionGroup,
  attempts,
  isSubmitting,
  isLoadingPokemon,
  isLoadingMorePokemon,
  hasMorePokemon,
  error,
  initialValues,
  onVersionGroupChange,
  onPokemonSearchChange,
  onLoadMorePokemon,
  onSubmit,
}: EncounterFormProps) {
  const [selectedPokemonSnapshot, setSelectedPokemonSnapshot] = useState<
    Pokemon | undefined
  >();
  const [pokemonId, setPokemonId] = useState<number | undefined>(
    initialValues?.pokemon_id,
  );
  const [maxHp, setMaxHp] = useState(initialValues?.max_hp ?? 100);
  const [currentHp, setCurrentHp] = useState(initialValues?.current_hp ?? 100);
  const [status, setStatus] = useState<StatusCondition>(
    initialValues?.status ?? "none",
  );
  const [ball, setBall] = useState<BallType>(initialValues?.ball ?? "poke_ball");
  const [playerPokemonLevel, setPlayerPokemonLevel] = useState(
    initialValues?.player_pokemon_level ?? 50,
  );
  const [wildPokemonLevel, setWildPokemonLevel] = useState(
    initialValues?.wild_pokemon_level ?? 30,
  );
  const [isFishingEncounter, setIsFishingEncounter] = useState(
    initialValues?.is_fishing_encounter ?? false,
  );
  const [isSurfingEncounter, setIsSurfingEncounter] = useState(
    initialValues?.is_surfing_encounter ?? false,
  );
  const [isUnderwaterEncounter, setIsUnderwaterEncounter] = useState(
    initialValues?.is_underwater_encounter ?? false,
  );
  const [isDarkLocation, setIsDarkLocation] = useState(
    initialValues?.is_dark_location ?? false,
  );
  const [hasCaughtSpeciesBefore, setHasCaughtSpeciesBefore] = useState(
    initialValues?.has_caught_species_before ?? false,
  );
  const [isSameSpecies, setIsSameSpecies] = useState(
    initialValues?.is_same_species ?? false,
  );
  const [isOppositeGender, setIsOppositeGender] = useState(
    initialValues?.is_opposite_gender ?? false,
  );
  const [turnsElapsed, setTurnsElapsed] = useState(
    initialValues?.turns_elapsed ?? 1,
  );

  const availableBallOptions =
    ballOptionsByVersionGroup[versionGroup] ?? ballOptionsByGeneration[generation];
  const selectedPokemon = pokemon.find((item) => item.id === pokemonId);
  const activePokemon = selectedPokemon ?? selectedPokemonSnapshot;
  const selectedBall = availableBallOptions.some((option) => option.value === ball)
    ? ball
    : (availableBallOptions[0]?.value ?? "poke_ball");
  const shouldShowBallContext = selectedBall in ballContextFieldsByBall;
  const activeBallContextFields = ballContextFieldsByBall[selectedBall] ?? [];

  function parsePositiveInt(value: string, fallback: number) {
    const nextValue = Number.parseInt(value, 10);

    if (!Number.isFinite(nextValue) || nextValue < 1) {
      return fallback;
    }

    return nextValue;
  }

  const getBallContextInput = useCallback(
    (ballType: BallType) => {
      switch (ballType) {
        case "love_ball":
          return {
            is_same_species: isSameSpecies,
            is_opposite_gender: isOppositeGender,
          };
        case "level_ball":
          return {
            player_pokemon_level: playerPokemonLevel,
            wild_pokemon_level: wildPokemonLevel,
          };
        case "lure_ball":
          return {
            is_fishing_encounter: isFishingEncounter,
          };
        case "net_ball":
          return {};
        case "dive_ball":
          return {
            is_fishing_encounter: isFishingEncounter,
            is_surfing_encounter: isSurfingEncounter,
            is_underwater_encounter: isUnderwaterEncounter,
          };
        case "nest_ball":
          return {
            wild_pokemon_level: wildPokemonLevel,
          };
        case "repeat_ball":
          return {
            has_caught_species_before: hasCaughtSpeciesBefore,
          };
        case "timer_ball":
        case "quick_ball":
          return {
            turns_elapsed: turnsElapsed,
          };
        case "dusk_ball":
          return {
            is_dark_location: isDarkLocation,
          };
        default:
          return {};
      }
    },
    [
      hasCaughtSpeciesBefore,
      isDarkLocation,
      isFishingEncounter,
      isOppositeGender,
      isSameSpecies,
      isSurfingEncounter,
      isUnderwaterEncounter,
      playerPokemonLevel,
      turnsElapsed,
      wildPokemonLevel,
    ],
  );

  const formError = useMemo(() => {
    if (!selectedPokemon) {
      return null;
    }

    if (currentHp > maxHp) {
      return "Los HP actuales no pueden superar los HP maximos.";
    }

    return null;
  }, [currentHp, maxHp, selectedPokemon]);

  const input = useMemo<CaptureCalculationInput | null>(() => {
    if (!activePokemon || formError) {
      return null;
    }

    return {
      pokemon_id: activePokemon.id,
      generation,
      version_group: versionGroup,
      max_hp: maxHp,
      current_hp: currentHp,
      status,
      ball: selectedBall,
      attempts,
      ...getBallContextInput(selectedBall),
    };
  }, [
    activePokemon,
    attempts,
    currentHp,
    formError,
    generation,
    getBallContextInput,
    maxHp,
    selectedBall,
    status,
    versionGroup,
  ]);

  useEffect(() => {
    if (!input) {
      return;
    }

    const timeoutId = window.setTimeout(() => {
      void onSubmit(input);
    }, 250);

    return () => {
      window.clearTimeout(timeoutId);
    };
  }, [input, onSubmit]);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Calculadora de captura</CardTitle>
        <CardDescription>
          Configura el encuentro y calcula la probabilidad de captura.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <div className="space-y-4">
          <Field label="Version" htmlFor="version-group">
            <Select
              value={versionGroup}
              onValueChange={(value) => {
                const nextVersionGroup = value as VersionGroup;
                const nextGeneration = getGenerationFromVersionGroup(nextVersionGroup);

                if (
                  activePokemon &&
                  !isPokemonAvailableInGeneration(activePokemon, nextGeneration)
                ) {
                  setSelectedPokemonSnapshot(undefined);
                  setPokemonId(undefined);
                }

                onPokemonSearchChange("");
                onVersionGroupChange(nextVersionGroup);
              }}
            >
              <SelectTrigger id="version-group" className="h-10 w-full px-3 text-sm">
                <SelectValue>
                  {versionGroupOptions.find((option) => option.value === versionGroup)?.label}
                </SelectValue>
              </SelectTrigger>
              <SelectContent align="start">
                {(Object.entries(versionGroupsByGeneration) as Array<
                  [string, Array<{ value: VersionGroup; label: string }>]
                >).map(([groupGeneration, options]) => (
                  <SelectGroup key={groupGeneration}>
                    <SelectLabel>Generacion {groupGeneration}</SelectLabel>
                    {options.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectGroup>
                ))}
              </SelectContent>
            </Select>
          </Field>

          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Pokemon" htmlFor="pokemon">
              <PokemonCombobox
                pokemon={pokemon}
                value={pokemonId}
                selectedPokemon={activePokemon}
                isLoading={isLoadingPokemon}
                isLoadingMore={isLoadingMorePokemon}
                hasMore={hasMorePokemon}
                onSearchChange={onPokemonSearchChange}
                onReachEnd={onLoadMorePokemon}
                onValueChange={(nextPokemonId) => {
                  const nextPokemon = pokemon.find((item) => item.id === nextPokemonId);
                  setSelectedPokemonSnapshot(nextPokemon);
                  setPokemonId(nextPokemonId);
                }}
              />
            </Field>

            <Field label="Pokeball" htmlFor="ball">
              <PokeballCombobox
                options={availableBallOptions}
                value={selectedBall}
                onValueChange={setBall}
              />
            </Field>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <Field label="HP maximos" htmlFor="max-hp">
              <Input
                id="max-hp"
                type="number"
                min={1}
                value={maxHp}
                onChange={(event) => {
                  const nextMaxHp = parsePositiveInt(event.target.value, 1);
                  setMaxHp(nextMaxHp);
                  setCurrentHp((previous) => Math.min(previous, nextMaxHp));
                }}
              />
            </Field>

            <Field label="HP actuales" htmlFor="current-hp">
              <Input
                id="current-hp"
                type="number"
                min={1}
                max={maxHp}
                value={currentHp}
                onChange={(event) => {
                  const nextCurrentHp = parsePositiveInt(event.target.value, 1);
                  setCurrentHp(Math.min(nextCurrentHp, maxHp));
                }}
              />
            </Field>

            <Field label="Estado" htmlFor="status">
              <Select value={status} onValueChange={(value) => setStatus(value as StatusCondition)}>
                <SelectTrigger id="status" className="h-10 w-full px-3 text-sm">
                  <SelectValue>{getOptionLabel(statusOptions, status)}</SelectValue>
                </SelectTrigger>
                <SelectContent align="start">
                  {statusOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      {option.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>
          </div>

          {shouldShowBallContext && (
            <Accordion
              type="single"
              collapsible
              value="ball-context"
              className="w-full"
            >
              <AccordionItem value="ball-context" className="border-b-0">
                <AccordionTrigger className="px-0 py-1 text-sm font-medium hover:no-underline">
                  Condiciones de {availableBallOptions.find((option) => option.value === selectedBall)?.label}
                </AccordionTrigger>
                <AccordionContent className="pt-3">
                  <div className="grid gap-4 sm:grid-cols-2">
                  {selectedBall === "love_ball" && (
                    <>
                      <CheckboxField
                        label="Misma especie"
                        checked={isSameSpecies}
                        onCheckedChange={setIsSameSpecies}
                      />
                      <CheckboxField
                        label="Genero opuesto"
                        checked={isOppositeGender}
                        onCheckedChange={setIsOppositeGender}
                      />
                    </>
                  )}

                  {selectedBall === "level_ball" && (
                    <>
                      <Field label="Nivel de tu Pokemon" htmlFor="player-pokemon-level">
                        <Input
                          id="player-pokemon-level"
                          type="number"
                          min={1}
                          max={100}
                          value={playerPokemonLevel}
                          onChange={(event) => {
                            setPlayerPokemonLevel(parsePositiveInt(event.target.value, 1));
                          }}
                        />
                      </Field>
                      <Field label="Nivel del salvaje" htmlFor="wild-pokemon-level">
                        <Input
                          id="wild-pokemon-level"
                          type="number"
                          min={1}
                          max={100}
                          value={wildPokemonLevel}
                          onChange={(event) => {
                            setWildPokemonLevel(parsePositiveInt(event.target.value, 1));
                          }}
                        />
                      </Field>
                    </>
                  )}

                  {selectedBall === "lure_ball" && (
                    <CheckboxField
                      label="Encuentro por pesca"
                      checked={isFishingEncounter}
                      onCheckedChange={setIsFishingEncounter}
                    />
                  )}

                  {selectedBall === "dive_ball" && (
                    <>
                      <CheckboxField
                        label="Encuentro por pesca"
                        checked={isFishingEncounter}
                        onCheckedChange={setIsFishingEncounter}
                      />
                      <CheckboxField
                        label="Encuentro surfeando"
                        checked={isSurfingEncounter}
                        onCheckedChange={setIsSurfingEncounter}
                      />
                      <CheckboxField
                        label="Encuentro bajo el agua"
                        checked={isUnderwaterEncounter}
                        onCheckedChange={setIsUnderwaterEncounter}
                      />
                    </>
                  )}

                  {selectedBall === "nest_ball" && (
                    <Field label="Nivel del salvaje" htmlFor="wild-pokemon-level-nest">
                      <Input
                        id="wild-pokemon-level-nest"
                        type="number"
                        min={1}
                        max={100}
                        value={wildPokemonLevel}
                        onChange={(event) => {
                          setWildPokemonLevel(parsePositiveInt(event.target.value, 1));
                        }}
                      />
                    </Field>
                  )}

                  {selectedBall === "repeat_ball" && (
                    <CheckboxField
                      label="Ya capturaste esta especie"
                      checked={hasCaughtSpeciesBefore}
                      onCheckedChange={setHasCaughtSpeciesBefore}
                    />
                  )}

                  {(selectedBall === "timer_ball" || selectedBall === "quick_ball") && (
                    <Field label="Turnos transcurridos" htmlFor="turns-elapsed">
                      <Input
                        id="turns-elapsed"
                        type="number"
                        min={1}
                        max={100}
                        value={turnsElapsed}
                        onChange={(event) => {
                          setTurnsElapsed(parsePositiveInt(event.target.value, 1));
                        }}
                      />
                    </Field>
                  )}

                  {selectedBall === "dusk_ball" && (
                    <CheckboxField
                      label="Cueva o zona oscura"
                      checked={isDarkLocation}
                      onCheckedChange={setIsDarkLocation}
                    />
                  )}
                </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          )}

          {(formError || error) && (
            <p className="text-sm text-destructive">{formError ?? error}</p>
          )}

        </div>
      </CardContent>
    </Card>
  );
}

function getGenerationFromVersionGroup(versionGroup: VersionGroup): Generation {
  const option = versionGroupOptions.find((item) => item.value === versionGroup);
  return option?.generation ?? 1;
}

function isPokemonAvailableInGeneration(
  pokemon: Pokemon,
  generation: Generation,
): boolean {
  const maxDexByGeneration: Record<Generation, number> = {
    1: 151,
    2: 251,
    3: 386,
    4: 493,
    5: 649,
    6: 721,
    7: 809,
    8: 905,
    9: 1025,
  };

  return pokemon.national_dex_number <= maxDexByGeneration[generation];
}

function Field({
  label,
  htmlFor,
  children,
}: {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-2">
      <label htmlFor={htmlFor} className="text-sm font-medium">
        {label}
      </label>
      {children}
    </div>
  );
}

function CheckboxField({
  label,
  checked,
  onCheckedChange,
}: {
  label: string;
  checked: boolean;
  onCheckedChange: (checked: boolean) => void;
}) {
  return (
    <label className="flex min-h-10 items-center gap-3 rounded-lg border border-border/60 bg-background px-3 py-2 text-sm">
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => {
          onCheckedChange(event.target.checked);
        }}
        className="size-4"
      />
      <span>{label}</span>
    </label>
  );
}
