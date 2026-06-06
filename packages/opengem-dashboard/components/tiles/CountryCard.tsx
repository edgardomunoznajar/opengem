import Link from "next/link";
import { isoToFlag, fmt, deltaSign, cn } from "@/lib/utils";
import { Sparkline } from "./Sparkline";

interface CountryCardProps {
  iso3: string;
  name: string;
  metrics: Array<{ label: string; value: number; unit?: string; delta?: number; spark?: number[] }>;
  recessionProb?: number;
  gpr?: number;
}

export function CountryCard({ iso3, name, metrics, recessionProb, gpr }: CountryCardProps) {
  return (
    <Link
      href={`/countries/${iso3}`}
      className="tile group block hover:border-line-strong"
    >
      <div className="flex items-baseline justify-between gap-2">
        <div className="flex items-baseline gap-2">
          <span className="text-base">{isoToFlag(iso3)}</span>
          <span className="font-mono text-2xs uppercase tracking-wider text-ink-muted">
            {iso3}
          </span>
          <span className="truncate text-sm">{name}</span>
        </div>
        {recessionProb !== undefined && (
          <span
            className={cn(
              "pill",
              recessionProb > 0.5 && "pill-bad",
              recessionProb > 0.25 && recessionProb <= 0.5 && "pill-warn",
              recessionProb <= 0.25 && "pill-good"
            )}
            title="12-month recession probability (Bauer-Mertens term-spread)"
          >
            R {(recessionProb * 100).toFixed(0)}%
          </span>
        )}
      </div>
      <div className="mt-2 grid grid-cols-3 gap-2">
        {metrics.slice(0, 3).map((m) => {
          const dir = deltaSign(m.delta);
          return (
            <div key={m.label} className="min-w-0">
              <div className="text-2xs uppercase tracking-wide text-ink-subtle">
                {m.label}
              </div>
              <div className="num text-base text-ink">{fmt(m.value, m.unit)}</div>
              {m.spark && (
                <Sparkline
                  data={m.spark}
                  trend={dir}
                  width={64}
                  height={14}
                  className={cn(
                    "mt-0.5",
                    dir === "up" && "text-good",
                    dir === "down" && "text-bad",
                    dir === "flat" && "text-ink-muted"
                  )}
                />
              )}
            </div>
          );
        })}
      </div>
      {gpr !== undefined && (
        <div className="mt-2 flex items-center justify-between text-2xs text-ink-subtle">
          <span>Geopolitical risk</span>
          <span className="num text-ink-muted">{gpr.toFixed(0)}</span>
        </div>
      )}
    </Link>
  );
}
