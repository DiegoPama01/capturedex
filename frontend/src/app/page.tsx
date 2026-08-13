import { CalculatorShell } from "@/features/capture-calculator/components/calculator-shell";
import { getPokemon } from "@/lib/api";

export default async function Home() {
  const response = await getPokemon();

  return (
    <main
      className="flex min-h-screen items-center justify-center bg-background p-6"
      style={{
        backgroundImage:
          "linear-gradient(rgba(188, 0, 7, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(188, 0, 7, 0.03) 1px, transparent 1px)",
        backgroundSize: "24px 24px",
      }}
    >
      <CalculatorShell pokemon={response.results} />
    </main>
  );
}
