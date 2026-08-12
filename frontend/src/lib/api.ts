const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api";

type HealthResponse = {
  status: string;
  application: string;
};

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_URL}/health/`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Django API is unavailable");
  }

  return response.json();
}