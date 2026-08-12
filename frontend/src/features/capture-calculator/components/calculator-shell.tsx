"use client";

import { useState } from "react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { PokemonCombobox } from "./pokemon-combobox";
import type {
  Pokemon,
} from "@/features/capture-calculator/types/capture";

type CalculatorShellProps = {
  pokemon: Pokemon[];
};

export function CalculatorShell({
  pokemon,
}: CalculatorShellProps) {
  const [pokemonId, setPokemonId] = useState<number>();

  const selectedPokemon = pokemon.find(
    (item) => item.id === pokemonId,
  );

  return (
    <Card className="w-full max-w-xl">
      <CardHeader>
        <CardTitle>Calculadora de captura</CardTitle>
        <CardDescription>
          Selecciona el Pokémon que quieres capturar.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        <PokemonCombobox
          pokemon={pokemon}
          value={pokemonId}
          onValueChange={setPokemonId}
        />

        {selectedPokemon && (
          <p className="text-sm text-muted-foreground">
            Tasa de captura:{" "}
            {selectedPokemon.generation_data[0]?.catch_rate}
          </p>
        )}
      </CardContent>
    </Card>
  );
}