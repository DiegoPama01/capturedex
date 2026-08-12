import { getHealth } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default async function Home() {
  const health = await getHealth();

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>{health.application}</CardTitle>
          <CardDescription>
            Pokémon capture probability calculator
          </CardDescription>
        </CardHeader>

        <CardContent>
          <Badge variant="secondary">
            API: {health.status}
          </Badge>
        </CardContent>
      </Card>
    </main>
  );
}