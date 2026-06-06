import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function fmt(n: number | undefined | null, unit?: string, digits = 1): string {
  if (n === undefined || n === null || Number.isNaN(n)) return "—";
  const s = n.toFixed(digits);
  return unit ? `${s}${unit === "%" ? "%" : ` ${unit}`}` : s;
}

export function deltaSign(d: number | undefined): "up" | "down" | "flat" {
  if (d === undefined || Math.abs(d) < 1e-9) return "flat";
  return d > 0 ? "up" : "down";
}

export function shortPct(n: number, digits = 1): string {
  return `${n >= 0 ? "+" : ""}${n.toFixed(digits)}%`;
}

export function isoToFlag(iso3: string): string {
  // ISO-3166-1 alpha-3 → emoji flag via alpha-2.
  // This is a partial map for prototype; production should use a lookup table.
  const a3to2: Record<string, string> = {
    USA: "US", CHN: "CN", JPN: "JP", DEU: "DE", GBR: "GB", FRA: "FR",
    IND: "IN", ITA: "IT", BRA: "BR", CAN: "CA", RUS: "RU", KOR: "KR",
    AUS: "AU", MEX: "MX", ESP: "ES", IDN: "ID", NLD: "NL", SAU: "SA",
    TUR: "TR", CHE: "CH", POL: "PL", ARG: "AR", SWE: "SE", BEL: "BE",
    IRL: "IE", ZAF: "ZA",
  };
  const a2 = a3to2[iso3];
  if (!a2) return "🌐";
  return String.fromCodePoint(
    ...a2.split("").map((c) => 0x1f1e6 - 65 + c.charCodeAt(0))
  );
}
