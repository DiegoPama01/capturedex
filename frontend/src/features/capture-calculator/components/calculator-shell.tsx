"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { CaptureResultCard } from "./capture-result-card";
import { EncounterForm } from "./encounter-form";
import type {
  CaptureCalculationInput,
  CaptureCalculationResponse,
  Pokemon,
} from "@/features/capture-calculator/types/capture";
import { calculateCapture, getPokemon } from "@/lib/api";

type CalculatorShellProps = {
  pokemon: Pokemon[];
};

export function CalculatorShell({
  pokemon,
}: CalculatorShellProps) {
  const [generation, setGeneration] = useState<1 | 2>(1);
  const [pokemonOptions, setPokemonOptions] = useState<Pokemon[]>(pokemon);
  const [pokemonSearch, setPokemonSearch] = useState("");
  const [pokemonPage, setPokemonPage] = useState(1);
  const [hasMorePokemon, setHasMorePokemon] = useState(false);
  const [result, setResult] =
    useState<CaptureCalculationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [isLoadingPokemon, setIsLoadingPokemon] = useState(false);
  const [isLoadingMorePokemon, setIsLoadingMorePokemon] = useState(false);
  const [attempts, setAttempts] = useState(1);
  const [lastEncounter, setLastEncounter] =
    useState<CaptureCalculationInput>();
  const requestIdRef = useRef(0);

  useEffect(() => {
    requestIdRef.current += 1;
    const requestId = requestIdRef.current;

    async function loadPokemon() {
      setIsLoadingPokemon(true);
      setError(null);

      try {
        const response = await getPokemon({
          search: pokemonSearch,
          generation,
          page: 1,
        });

        if (requestId !== requestIdRef.current) {
          return;
        }

        setPokemonOptions(response.results);
        setPokemonPage(1);
        setHasMorePokemon(response.next !== null);
        setResult(null);
        setLastEncounter(undefined);
      } catch {
        if (requestId !== requestIdRef.current) {
          return;
        }

        setPokemonOptions([]);
        setPokemonPage(1);
        setHasMorePokemon(false);
        setResult(null);
        setLastEncounter(undefined);
        setError("No se pudo cargar la lista de Pokemon.");
      } finally {
        if (requestId === requestIdRef.current) {
          setIsLoadingPokemon(false);
        }
      }
    }

    void loadPokemon();
  }, [generation, pokemonSearch]);

  const handleLoadMorePokemon = useCallback(async () => {
    if (isLoadingPokemon || isLoadingMorePokemon || !hasMorePokemon) {
      return;
    }

    const nextPage = pokemonPage + 1;
    setIsLoadingMorePokemon(true);

    try {
      const response = await getPokemon({
        search: pokemonSearch,
        generation,
        page: nextPage,
      });

      setPokemonOptions((current) => [...current, ...response.results]);
      setPokemonPage(nextPage);
      setHasMorePokemon(response.next !== null);
    } catch {
      setError("No se pudo cargar mas Pokemon.");
    } finally {
      setIsLoadingMorePokemon(false);
    }
  }, [generation, hasMorePokemon, isLoadingMorePokemon, isLoadingPokemon, pokemonPage, pokemonSearch]);

  const handleCalculate = useCallback(async (input: CaptureCalculationInput) => {
    setIsCalculating(true);
    setError(null);
    setAttempts(input.attempts);
    setLastEncounter(input);

    try {
      const nextResult = await calculateCapture(input);

      setResult(nextResult);
    } catch {
      setResult(null);
      setError("No se pudo calcular la captura. Intentalo de nuevo.");
    } finally {
      setIsCalculating(false);
    }
  }, []);

  async function handleAttemptsChange(nextAttempts: number) {
    if (!lastEncounter || nextAttempts === attempts) {
      return;
    }

    await handleCalculate({
      ...lastEncounter,
      attempts: nextAttempts,
    });
  }

  return (
    <div className="grid w-full max-w-5xl gap-6 lg:grid-cols-[minmax(0,1fr)_420px] lg:items-start">
      <EncounterForm
        pokemon={pokemonOptions}
        generation={generation}
        attempts={attempts}
        isSubmitting={isCalculating || isLoadingPokemon}
        isLoadingPokemon={isLoadingPokemon}
        isLoadingMorePokemon={isLoadingMorePokemon}
        hasMorePokemon={hasMorePokemon}
        error={error}
        initialValues={lastEncounter}
        onGenerationChange={setGeneration}
        onPokemonSearchChange={setPokemonSearch}
        onLoadMorePokemon={handleLoadMorePokemon}
        onSubmit={handleCalculate}
      />

      <CaptureResultCard
        result={result}
        generation={generation}
        attempts={attempts}
        isUpdatingAttempts={isCalculating}
        onAttemptsChange={handleAttemptsChange}
      />
    </div>
  );
}
