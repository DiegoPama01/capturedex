import { CalculatorShell } from "@/features/capture-calculator/components/calculator-shell";
import { getPokemon } from "@/lib/api";

export default async function Home() {
  const response = await getPokemon();

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <CalculatorShell pokemon={response.results} />
    </main>
  );
}