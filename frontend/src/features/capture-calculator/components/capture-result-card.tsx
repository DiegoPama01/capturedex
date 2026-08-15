import Image from "next/image";
import {
  RiCheckboxCircleLine,
  RiFocus3Line,
  RiQuestionLine,
} from "@remixicon/react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import type {
  CaptureCalculationResponse,
  VersionGroup,
} from "../types/capture";

type CaptureResultCardProps = {
  result: CaptureCalculationResponse | null;
  versionGroup: VersionGroup;
  attempts: number;
  isUpdatingAttempts?: boolean;
  onAttemptsChange?: (attempts: number) => void;
};

export function CaptureResultCard({
  result,
  versionGroup,
  attempts,
  isUpdatingAttempts = false,
  onAttemptsChange,
}: CaptureResultCardProps) {
  if (!result) {
    return (
      <Card className="flex min-h-96 items-center justify-center">
        <CardContent className="flex flex-col items-center gap-3 text-center">
          <div className="rounded-full bg-muted p-4">
            <RiQuestionLine className="size-8 text-muted-foreground" />
          </div>

          <div>
            <p className="font-medium">Aún no hay ningún cálculo</p>
            <p className="mt-1 max-w-xs text-sm text-muted-foreground">
              Configura el encuentro y pulsa en calcular para ver tus
              probabilidades.
            </p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const singleProbability = toPercentage(
    result.result.single_throw_probability,
  );

  const cumulativeProbability = toPercentage(
    result.result.cumulative_probability,
  );

  return (
    <Card className="overflow-hidden">
      <CardHeader className="items-center text-center">
        <Badge variant="secondary">{getVersionGroupLabel(versionGroup)}</Badge>

        {result.pokemon.sprite_url && (
          <Image
            src={result.pokemon.sprite_url}
            alt={result.pokemon.name}
            width={144}
            height={144}
            className="mx-auto size-36 object-contain [image-rendering:pixelated]"
          />
        )}

        <CardTitle className="text-2xl">{result.pokemon.name}</CardTitle>

        <CardDescription>
          #{String(result.pokemon.national_dex_number).padStart(3, "0")}
          {" · "}
          Tasa de captura {result.pokemon.catch_rate}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-6">
        {result.result.guaranteed ? (
          <div className="flex items-center justify-center gap-2 rounded-xl bg-green-500/10 p-4 text-green-700 dark:text-green-400">
            <RiCheckboxCircleLine className="size-5" />
            <span className="font-semibold">Captura garantizada</span>
          </div>
        ) : (
          <SingleProbabilitySection
            probability={singleProbability}
          />
        )}

        <CumulativeProbabilitySection
          attempts={attempts}
          probability={cumulativeProbability}
          isUpdatingAttempts={isUpdatingAttempts}
          onAttemptsChange={onAttemptsChange}
        />

        <div className="grid grid-cols-2 gap-3">
          <ResultMetric
            label="Lanzamientos esperados"
            value={formatExpectedThrows(result.result.expected_throws)}
          />

          <ResultMetric
            label="Tasa base"
            value={String(result.pokemon.catch_rate)}
          />
        </div>

        {!result.result.guaranteed && (
          <p className="text-center text-xs text-muted-foreground">
            Cada lanzamiento se considera un intento independiente.
          </p>
        )}
      </CardContent>
    </Card>
  );
}

type CumulativeProbabilitySectionProps = {
  attempts: number;
  probability: number;
  isUpdatingAttempts?: boolean;
  onAttemptsChange?: (attempts: number) => void;
};

function SingleProbabilitySection({ probability }: { probability: number }) {
  return (
    <div className="space-y-2">
      <div className="flex items-end justify-between gap-4">
        <span className="text-sm text-muted-foreground">
          Probabilidad por lanzamiento
        </span>

        <span className="text-3xl font-bold tracking-tight">
          {probability.toFixed(2)}%
        </span>
      </div>

      <Progress value={probability} />
    </div>
  );
}

function getVersionGroupLabel(versionGroup: VersionGroup): string {
  if (versionGroup === "red-blue") {
    return "Red / Blue";
  }

  if (versionGroup === "gold-silver") {
    return "Gold / Silver";
  }

  if (versionGroup === "crystal") {
    return "Crystal";
  }

  if (versionGroup === "ruby-sapphire") {
    return "Ruby / Sapphire";
  }

  if (versionGroup === "emerald") {
    return "Emerald";
  }

  if (versionGroup === "firered-leafgreen") {
    return "FireRed / LeafGreen";
  }

  if (versionGroup === "diamond-pearl") {
    return "Diamond / Pearl";
  }

  if (versionGroup === "platinum") {
    return "Platinum";
  }

  if (versionGroup === "heartgold-soulsilver") {
    return "HeartGold / SoulSilver";
  }

  if (versionGroup === "black-white") {
    return "Black / White";
  }

  return "Black 2 / White 2";
}

function CumulativeProbabilitySection({
  attempts,
  probability,
  isUpdatingAttempts = false,
  onAttemptsChange,
}: CumulativeProbabilitySectionProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-end justify-between gap-4">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span>Probabilidad tras</span>
          <Input
            type="number"
            min={1}
            value={attempts}
            disabled={isUpdatingAttempts}
            onChange={(event) => {
              const value = Number.parseInt(event.target.value, 10);

              if (Number.isFinite(value) && value > 0) {
                onAttemptsChange?.(value);
              }
            }}
            className="h-8 w-14 px-1.5 text-center text-sm"
          />
          <span>{attempts === 1 ? "lanzamiento" : "lanzamientos"}</span>
        </div>

        <span className="text-xl font-semibold">
          {probability.toFixed(2)}%
        </span>
      </div>

      <Progress value={probability} />
    </div>
  );
}

function ResultMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border bg-muted/30 p-4 text-center">
      <RiFocus3Line className="mx-auto mb-2 size-4 text-muted-foreground" />
      <p className="text-lg font-semibold">{value}</p>
      <p className="text-xs text-muted-foreground">{label}</p>
    </div>
  );
}

function toPercentage(probability: number): number {
  return Math.min(100, Math.max(0, probability * 100));
}

function formatExpectedThrows(value: number): string {
  if (!Number.isFinite(value)) {
    return "∞";
  }

  return value.toFixed(2);
}
