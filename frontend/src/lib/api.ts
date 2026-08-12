import type {
  CaptureCalculationInput,
  CaptureCalculationResponse,
  PokemonListResponse,
} from "@/features/capture-calculator/types/capture";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000/api/v1";

export async function getPokemon(
  search = "",
): Promise<PokemonListResponse> {
  const params = new URLSearchParams();

  if (search) {
    params.set("search", search);
  }

  const query = params.toString();
  const url = `${API_URL}/pokemon/${query ? `?${query}` : ""}`;

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
    `${API_URL}/captures/calculate/`,
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