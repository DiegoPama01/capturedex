"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

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
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type {
  BallType,
  CaptureCalculationInput,
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
  generation: 1 | 2;
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

const versionGroupOptions: Array<{ value: VersionGroup; label: string }> = [
  { value: "red-blue", label: "Red / Blue" },
  { value: "gold-silver", label: "Gold / Silver" },
  { value: "crystal", label: "Crystal" },
] as const;

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

const ballOptions: PokeballOption[] = [
  {
    value: "poke_ball",
    label: "Poke Ball",
    sprite: "/pokeballs/Poké_Ball.png",
  },
  {
    value: "great_ball",
    label: "Great Ball",
    sprite: "/pokeballs/Super_Ball.png",
  },
  {
    value: "ultra_ball",
    label: "Ultra Ball",
    sprite: "/pokeballs/Ultra_Ball.png",
  },
  {
    value: "master_ball",
    label: "Master Ball",
    sprite: "/pokeballs/Master_Ball.png",
  },
];

const generationTwoOnlyBallOptions: PokeballOption[] = [
  {
    value: "friend_ball",
    label: "Amigo Ball",
    sprite: "/pokeballs/Amigo_Ball.png",
  },
  {
    value: "moon_ball",
    label: "Luna Ball",
    sprite: "/pokeballs/Luna_Ball.png",
  },
  {
    value: "fast_ball",
    label: "Rapid Ball",
    sprite: "/pokeballs/Rapid_Ball.png",
  },
  {
    value: "love_ball",
    label: "Amor Ball",
    sprite: "/pokeballs/Amor_Ball.png",
  },
  {
    value: "level_ball",
    label: "Nivel Ball",
    sprite: "/pokeballs/Nivel_Ball.png",
  },
  {
    value: "lure_ball",
    label: "Cebo Ball",
    sprite: "/pokeballs/Cebo_Ball.png",
  },
  {
    value: "sport_ball",
    label: "Competi Ball",
    sprite: "/pokeballs/Competi_Ball.png",
  },
  {
    value: "heavy_ball",
    label: "Peso Ball",
    sprite: "/pokeballs/Peso_Ball.png",
  },
];

const ballOptionsByGeneration: Record<1 | 2, PokeballOption[]> = {
  1: ballOptions,
  2: [...ballOptions, ...generationTwoOnlyBallOptions],
};

const generationTwoContextBallSet = new Set<BallType>([
  "love_ball",
  "level_ball",
  "lure_ball",
]);

function getOptionLabel<T extends string>(
  options: Array<{ value: T; label: string }>,
  value: T,
) {
  return options.find((option) => option.value === value)?.label ?? value;
}

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
  const [selectedPokemonSnapshot, setSelectedPokemonSnapshot] = useState<Pokemon | undefined>();
  const [pokemonId, setPokemonId] = useState<number | undefined>(
    initialValues?.pokemon_id,
  );
  const [maxHp, setMaxHp] = useState(initialValues?.max_hp ?? 100);
  const [currentHp, setCurrentHp] = useState(
    initialValues?.current_hp ?? 100,
  );
  const [status, setStatus] = useState<StatusCondition>(
    initialValues?.status ?? "none",
  );
  const [ball, setBall] = useState<BallType>(
    initialValues?.ball ?? "poke_ball",
  );
  const [playerPokemonLevel, setPlayerPokemonLevel] = useState(
    initialValues?.player_pokemon_level ?? 50,
  );
  const [wildPokemonLevel, setWildPokemonLevel] = useState(
    initialValues?.wild_pokemon_level ?? 30,
  );
  const [isFishingEncounter, setIsFishingEncounter] = useState(
    initialValues?.is_fishing_encounter ?? false,
  );
  const [isSameSpecies, setIsSameSpecies] = useState(
    initialValues?.is_same_species ?? false,
  );
  const [isOppositeGender, setIsOppositeGender] = useState(
    initialValues?.is_opposite_gender ?? false,
  );

  const availableBallOptions = ballOptionsByGeneration[generation];

  const selectedPokemon = pokemon.find((item) => item.id === pokemonId);
  const activePokemon = selectedPokemon ?? selectedPokemonSnapshot;
  const selectedBall = availableBallOptions.some((option) => option.value === ball)
    ? ball
    : (availableBallOptions[0]?.value ?? "poke_ball");
  const shouldShowBallContext =
    generation === 2 && generationTwoContextBallSet.has(selectedBall);

  function parsePositiveInt(value: string, fallback: number) {
    const nextValue = Number.parseInt(value, 10);

    if (!Number.isFinite(nextValue) || nextValue < 1) {
      return fallback;
    }

    return nextValue;
  }

  const getBallContextInput = useCallback((ballType: BallType) => {
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
      default:
        return {};
    }
  }, [
    isFishingEncounter,
    isOppositeGender,
    isSameSpecies,
    playerPokemonLevel,
    wildPokemonLevel,
  ]);

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
    maxHp,
    selectedBall,
    status,
    versionGroup,
    getBallContextInput,
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
          <Field label="Versión" htmlFor="version-group">
            <Select
              value={versionGroup}
              onValueChange={(value) => {
                const nextVersionGroup = value as VersionGroup;
                const nextGeneration = nextVersionGroup === "red-blue" ? 1 : 2;

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
                {versionGroupOptions.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
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

          {activePokemon && (
            <p className="text-sm text-muted-foreground">
              Tasa de captura: {activePokemon.generation_data[0]?.catch_rate ?? "-"} · Versión: {versionGroupOptions.find((option) => option.value === versionGroup)?.label}
            </p>
          )}

          <div className="grid gap-4 sm:grid-cols-2">
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
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Estado" htmlFor="status">
              <Select
                value={status}
                onValueChange={(value) => setStatus(value as StatusCondition)}
              >
                <SelectTrigger id="status" className="h-10 w-full px-3 text-sm">
                  <SelectValue>
                    {getOptionLabel(statusOptions, status)}
                  </SelectValue>
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
            <div className="grid gap-4 rounded-xl border border-border/60 bg-muted/20 p-4 sm:grid-cols-2">
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
                        setPlayerPokemonLevel(
                          parsePositiveInt(event.target.value, 1),
                        );
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
                        setWildPokemonLevel(
                          parsePositiveInt(event.target.value, 1),
                        );
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
            </div>
          )}

          {(formError || error) && (
            <p className="text-sm text-destructive">{formError ?? error}</p>
          )}

          {activePokemon && !formError && (
            <p className="text-xs text-muted-foreground">
              {isSubmitting ? "Recalculando..." : "Se recalcula automaticamente al cambiar los valores."}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function isPokemonAvailableInGeneration(pokemon: Pokemon, generation: 1 | 2): boolean {
  const maxDexByGeneration = {
    1: 151,
    2: 251,
  } as const;

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
