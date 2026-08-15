import type {
  CaptureCalculationInput,
  CaptureCalculationResponse,
  PokemonListResponse,
  VersionGroup,
} from "@/features/capture-calculator/types/capture";

const PUBLIC_API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "/api/v1";

const INTERNAL_API_URL =
  process.env.INTERNAL_API_URL ??
  "http://capturedex-backend:8000/api/v1";

function getApiUrl() {
  return typeof window === "undefined"
    ? INTERNAL_API_URL
    : PUBLIC_API_URL;
}

type GetPokemonParams = {
  search?: string;
  generation?: 1 | 2;
  versionGroup?: VersionGroup;
  page?: number;
};

export async function getPokemon({
  search = "",
  generation,
  versionGroup,
  page,
}: GetPokemonParams = {}): Promise<PokemonListResponse> {
  const params = new URLSearchParams();

  if (search) params.set("search", search);
  if (generation) params.set("generation", String(generation));
  if (versionGroup) params.set("version_group", versionGroup);
  if (page) params.set("page", String(page));

  const query = params.toString();
  const url = `${getApiUrl()}/pokemon/${query ? `?${query}` : ""}`;

  const response = await fetch(url, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Could not load Pokémon.");
  }

  return response.json();
}

export async function calculateCapture(
  input: CaptureCalculationInput,
): Promise<CaptureCalculationResponse> {
  const response = await fetch(
    `${getApiUrl()}/captures/calculate/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(input),
    },
  );

  if (!response.ok) {
    throw new Error("Could not calculate capture probability.");
  }

  return response.json();
}