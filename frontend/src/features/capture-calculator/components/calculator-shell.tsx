"use client";

import { useCallback, useState } from "react";
import { CaptureResultCard } from "./capture-result-card";
import { EncounterForm } from "./encounter-form";
import type {
  CaptureCalculationInput,
  CaptureCalculationResponse,
  Pokemon,
} from "@/features/capture-calculator/types/capture";
import { calculateCapture } from "@/lib/api";

type CalculatorShellProps = {
  pokemon: Pokemon[];
};

export function CalculatorShell({
  pokemon,
}: CalculatorShellProps) {
  const [result, setResult] =
    useState<CaptureCalculationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [attempts, setAttempts] = useState(1);
  const [lastEncounter, setLastEncounter] =
    useState<CaptureCalculationInput>();

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
        pokemon={pokemon}
        attempts={attempts}
        isSubmitting={isCalculating}
        error={error}
        initialValues={lastEncounter}
        onSubmit={handleCalculate}
      />

      <CaptureResultCard
        result={result}
        attempts={attempts}
        isUpdatingAttempts={isCalculating}
        onAttemptsChange={handleAttemptsChange}
      />
    </div>
  );
}
