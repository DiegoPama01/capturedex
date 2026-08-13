"use client";

import { useEffect, useMemo, useState } from "react";

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
} from "@/features/capture-calculator/types/capture";
import { PokemonCombobox } from "./pokemon-combobox";
import {
  PokeballCombobox,
  type PokeballOption,
} from "./pokeball-combobox";

type EncounterFormProps = {
  pokemon: Pokemon[];
  attempts: number;
  isSubmitting: boolean;
  error: string | null;
  initialValues?: CaptureCalculationInput;
  onSubmit: (input: CaptureCalculationInput) => Promise<void> | void;
};

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

function getOptionLabel<T extends string>(
  options: Array<{ value: T; label: string }>,
  value: T,
) {
  return options.find((option) => option.value === value)?.label ?? value;
}

export function EncounterForm({
  pokemon,
  attempts,
  isSubmitting,
  error,
  initialValues,
  onSubmit,
}: EncounterFormProps) {
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

  const selectedPokemon = pokemon.find((item) => item.id === pokemonId);

  function parsePositiveInt(value: string, fallback: number) {
    const nextValue = Number.parseInt(value, 10);

    if (!Number.isFinite(nextValue) || nextValue < 1) {
      return fallback;
    }

    return nextValue;
  }

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
    if (!selectedPokemon || formError) {
      return null;
    }

    return {
      pokemon_id: selectedPokemon.id,
      generation: 1,
      max_hp: maxHp,
      current_hp: currentHp,
      status,
      ball,
      attempts,
    };
  }, [attempts, ball, currentHp, formError, maxHp, selectedPokemon, status]);

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
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Pokemon" htmlFor="pokemon">
              <PokemonCombobox
                pokemon={pokemon}
                value={pokemonId}
                onValueChange={(nextPokemonId) => {
                  setPokemonId(nextPokemonId);
                }}
              />
            </Field>

            <Field label="Pokeball" htmlFor="ball">
              <PokeballCombobox
                options={ballOptions}
                value={ball}
                onValueChange={setBall}
              />
            </Field>
          </div>

          {selectedPokemon && (
            <p className="text-sm text-muted-foreground">
              Tasa de captura: {selectedPokemon.generation_data[0]?.catch_rate}
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

          {(formError || error) && (
            <p className="text-sm text-destructive">{formError ?? error}</p>
          )}

          {selectedPokemon && !formError && (
            <p className="text-xs text-muted-foreground">
              {isSubmitting ? "Recalculando..." : "Se recalcula automaticamente al cambiar los valores."}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
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
