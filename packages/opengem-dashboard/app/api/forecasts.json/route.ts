import { NextResponse } from "next/server";
import { getForecasts } from "@/lib/api";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const country = searchParams.get("country") ?? undefined;
  const indicator = searchParams.get("indicator") ?? undefined;
  const horizon = searchParams.get("horizon") ?? undefined;

  const forecasts = await getForecasts({ country, indicator, horizon });

  return NextResponse.json(
    {
      generated_at: new Date().toISOString(),
      count: forecasts.length,
      license: "CC-BY-4.0",
      attribution: "OPENGEM (opengem.org)",
      forecasts,
    },
    {
      headers: {
        // Allow embedding scripts to consume from anywhere
        "Access-Control-Allow-Origin": "*",
        // Vintage-stamp the response
        "X-OPENGEM-Vintage": forecasts[0]?.vintage_id ?? "unknown",
        // Encourage caching
        "Cache-Control": "public, max-age=300, s-maxage=600",
      },
    }
  );
}
